import os, errno
import subprocess
import git
import shutil
import argparse


def args():
    parser = argparse.ArgumentParser("Code duplication finder")
    parser.add_argument("--repo_list", default="repos.txt")
    parser.add_argument("--token", default=None)
    parser.add_argument("--clone-dir", default="clones")
    parser.add_argument("--output", default="clone.xml")
    parser.add_argument("--language", default="scala")

    args = parser.parse_args()
    return args


def parse_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()


def make_dir(dirname):
    try:
        os.makedirs(target_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    

def clone_repo(repo_url, token):
    url_prefix = token + ":x-oauth-basic@"
    http_index = len("https://")
    updated_url = repo_url[:http_index] + url_prefix + repo_url[http_index:]
    git.Git().clone(updated_url)


def crawl_repos(target_dir, filename, token):
    saved_path = os.getcwd()
    repo_urls = parse_file(os.path.join(saved_path, filename))

    os.chdir(target_dir)
    for repo in repo_urls:
        clone_repo(repo, token)
    os.chdir(saved_path)


def run_cpd(parent_dir, language):
    cmd = "cpd --minimum-tokens 100 --files " + parent_dir + " --language " + language + " --format xml --failOnViolation false"
    try:
        with open(os.devnull, 'w')  as FNULL:
            output_bytes = subprocess.check_output(['/bin/bash', '-i', '-c', cmd], stderr=FNULL)
            output = output_bytes.decode("utf-8")
        return output
    except subprocess.CalledProcessError as e:
        print(e)
        return None


def write_output(content, target):
    with open(target, 'w') as f:
        f.write(content.encode("utf-8"))


if __name__ == "__main__":
    args = args()
    target_dir = args.clone_dir
    if args.token:
        token = args.token
    else:
        token=os.environ["GITHUB_ACCESS_TOKEN"]
    make_dir(target_dir)
    try:
        crawl_repos(target_dir, args.repo_list, token)
        output = run_cpd(target_dir, args.language)
        write_output(output, args.output)
    finally:
        shutil.rmtree(target_dir)
