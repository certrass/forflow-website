#!/usr/bin/env python3
"""GitHub project status and explicit, verified push. Python standard library only."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys


class Failure(Exception):
    pass


def run(argv, cwd=None, env=None, timeout=30):
    try:
        return subprocess.run(argv, cwd=cwd, env=env, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=timeout)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(argv, 124, '', 'command timed out')
    except OSError as exc:
        return subprocess.CompletedProcess(argv, 127, '', str(exc))


def clean(text):
    text = re.sub(r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]+', '[REDACTED]', text)
    return re.sub(r'://[^/@\s]+@', '://[REDACTED]@', text)


def require(result):
    if result.returncode:
        raise Failure(clean((result.stderr or result.stdout).strip()))
    return result.stdout.strip()


def git(root, *args):
    return run(['git', '-C', str(root), *args])


def transient(result):
    message = (result.stderr + result.stdout).lower()
    return result.returncode == 124 or any(term in message for term in (
        'timed out', 'connection refused', 'could not resolve', 'failed to connect',
        'connection reset', 'unexpected eof', ': eof', 'tls handshake timeout',
        'remote end hung up', 'http 502', 'http 503', 'http 504', 'empty reply'))


def routes():
    base = dict(os.environ, GIT_TERMINAL_PROMPT='0', GH_PROMPT_DISABLED='1')
    proxy_keys = ('http_proxy', 'https_proxy', 'all_proxy', 'no_proxy')
    direct = {k: v for k, v in base.items() if k.lower() not in proxy_keys}
    direct['NO_PROXY'] = 'localhost,127.0.0.1,::1'
    result = []
    if sys.platform == 'darwin':
        state = run(['/usr/sbin/scutil', '--proxy'], timeout=5).stdout
        fields = dict(re.findall(r'^\s*(\w+)\s*:\s*(\S+)\s*$', state, re.M))
        prefix = 'HTTPS' if fields.get('HTTPSEnable') == '1' else 'HTTP'
        if fields.get(prefix + 'Enable') == '1':
            host, port = fields.get(prefix + 'Proxy'), fields.get(prefix + 'Port')
            if host and port and port.isdigit():
                proxy = 'http://' + host + ':' + port
                env = dict(direct, HTTP_PROXY=proxy, HTTPS_PROXY=proxy)
                result.append(('当前系统代理', env, proxy))
    inherited = base.get('https_proxy') or base.get('HTTPS_PROXY') or ''
    if inherited:
        result.append(('当前任务代理', base, inherited))
    result.append(('直接连接', direct, ''))
    seen = set()
    return [r for r in result if not (r[2] in seen or seen.add(r[2]))]


class Network:
    def __init__(self, root):
        self.root = root
        self.options = routes()
        self.selected = None

    def command(self, args, route, timeout=30):
        label, env, proxy = route
        if args[0] == 'git':
            args = ['git', '-c', 'http.proxy=' + proxy,
                    '-c', 'http.https://github.com.proxy=' + proxy, *args[1:]]
        return run(args, cwd=self.root, env=env, timeout=timeout)

    def read(self, args, timeout=30):
        options = self.options if self.selected is None else [self.selected] + [
            r for r in self.options if r != self.selected]
        for route in options:
            result = self.command(args, route, timeout)
            if result.returncode == 0:
                if route != self.selected:
                    print('连接路径：' + route[0], flush=True)
                self.selected = route
                return result
            if not transient(result):
                return result
            print(route[0] + '暂时失败，尝试下一条连接路径。', flush=True)
        return result


def context(path):
    result = git(path, 'rev-parse', '--show-toplevel')
    if result.returncode:
        raise Failure('此目录没有 Git 仓库。请进入已关联 GitHub 的项目后执行。')
    root = Path(result.stdout.strip())
    remote_result = git(root, 'remote', 'get-url', '--push', 'origin')
    if remote_result.returncode:
        raise Failure('此项目尚未配置 origin 远程仓库；登录 GitHub 不会自动关联项目。')
    remote = remote_result.stdout.strip()
    match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/\s]+/[^/\s]+?)(?:\.git)?', remote)
    if not match:
        raise Failure('origin 不是支持的 GitHub 地址，请先核对项目与远程仓库。')
    head = require(git(root, 'rev-parse', '--verify', 'HEAD'))
    branch = require(git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD'))
    return root, remote, match.group(1), head, branch


def remote_head(net, remote, branch):
    text = require(net.read(['git', 'ls-remote', '--heads', remote, 'refs/heads/' + branch]))
    return text.split()[0] if text else None


def check(root, remote, slug, head, branch, net):
    print('项目：' + str(root))
    print('仓库：https://github.com/' + slug)
    print('分支：' + branch + '\n本地提交：' + head, flush=True)
    status = require(git(root, 'status', '--porcelain=v1', '-uall'))
    entries = status.splitlines() if status else []
    print('未提交文件：' + str(len(entries)) + '（这些修改尚未包含在上传版本里）')
    metadata = json.loads(require(net.read([
        'gh', 'api', 'repos/' + slug, '--jq',
        '{full_name,private,default_branch,permissions}'])))
    if not metadata.get('permissions', {}).get('push'):
        raise Failure('当前 GitHub 账号没有该仓库的 push 权限。')
    print('默认分支：' + metadata['default_branch'])
    remote_sha = remote_head(net, remote, branch)
    print('远端提交：' + (remote_sha or '此分支尚未上传'))
    if remote_sha == head:
        print('当前已提交版本与远端一致。')
    elif remote_sha and git(root, 'cat-file', '-e', remote_sha + '^{commit}').returncode == 0:
        counts = require(git(root, 'rev-list', '--left-right', '--count', head + '...' + remote_sha)).split()
        print('本地独有提交：' + counts[0] + '；远端独有提交：' + counts[1])
        pending = require(git(root, 'log', '--oneline', remote_sha + '..' + head))
        if pending:
            print(pending)
    elif remote_sha:
        print('本地尚未读取远端提交对象；上传预检将检查是否允许快进。')
    return remote_sha


def preflight(root, remote, head, branch, old_sha, net):
    print('\n上传预检：' + head[:12] + ' → ' + branch, flush=True)
    revision = head
    if old_sha and git(root, 'cat-file', '-e', old_sha + '^{commit}').returncode == 0:
        revision = old_sha + '..' + head
    objects = require(git(root, 'rev-list', '--objects', revision))
    if objects:
        try:
            sizes = subprocess.run(
                ['git', 'cat-file', '--batch-check=%(objecttype) %(objectsize) %(rest)'],
                input=objects + '\n', cwd=root, text=True, capture_output=True, timeout=30)
        except subprocess.TimeoutExpired:
            raise Failure('检查待上传对象大小超时；尚未上传。')
        for line in require(sizes).splitlines():
            kind, size, *name = line.split(' ', 2)
            if kind == 'blob' and int(size) > 100 * 1024 * 1024:
                raise Failure('提交包含超过 100 MiB 的文件：' + ''.join(name) + '。请先处理大文件存储。')
    result = net.read(['git', 'push', '--dry-run', '--porcelain', remote,
                       head + ':refs/heads/' + branch], timeout=45)
    require(result)
    print('预检通过；尚未上传。', flush=True)


def publish(root, remote, head, branch, net, approved_head=None,
            approved_remote=None, approved_branch=None):
    approved = (approved_head, approved_remote, approved_branch)
    if any(approved) and (not all(approved) or approved != (head, remote, branch)):
        raise Failure('上传授权必须同时匹配完整提交 SHA、远程地址和分支；目标不一致，尚未上传。')
    if approved_head is None:
        print('\n将上传上述已提交版本到 ' + remote + ' 的 ' + branch + ' 分支。')
        if not sys.stdin.isatty():
            raise Failure('非交互执行须在已有上传授权后同时传入 --approved-head、--approved-remote 和 --approved-branch。')
        if input('输入 push 确认上传，其他输入取消：').strip() != 'push':
            print('已取消上传。')
            return
    if require(git(root, 'rev-parse', 'HEAD')) != head:
        raise Failure('检查后本地 HEAD 已变化，请重新预检。')
    if require(git(root, 'symbolic-ref', '--quiet', '--short', 'HEAD')) != branch:
        raise Failure('检查后当前分支已变化，尚未上传。')
    if require(git(root, 'remote', 'get-url', '--push', 'origin')) != remote:
        raise Failure('检查后远程地址已变化，尚未上传。')
    print('正在上传 ' + head[:12] + '…', flush=True)
    # Mutations are attempted once. An ambiguous result is resolved by reading the remote.
    result = net.command(['git', 'push', '--porcelain', remote,
                          head + ':refs/heads/' + branch], net.selected, timeout=180)
    actual = remote_head(net, remote, branch)
    if actual != head:
        if result.returncode:
            raise Failure('上传未确认成功：' + clean(result.stderr or result.stdout) +
                          '\n远端当前版本：' + (actual or '分支不存在'))
        raise Failure('上传后远端已变化，当前版本：' + (actual or '分支不存在') + '。请检查并发更新。')
    print('上传完成，远端回读一致：' + actual)
    # Keep the app's local tracking state aligned without changing the working tree.
    fetch_url = git(root, 'remote', 'get-url', 'origin').stdout.strip()
    push_url = git(root, 'remote', 'get-url', '--push', 'origin').stdout.strip()
    if fetch_url == push_url == remote:
        ref = 'refs/remotes/origin/' + branch
        previous = git(root, 'rev-parse', '--verify', ref).stdout.strip() or '0' * len(head)
        updated = git(root, 'update-ref', ref, actual, previous)
        if updated.returncode == 0:
            existing = git(root, 'config', '--get', 'branch.' + branch + '.remote')
            branch_head = git(root, 'rev-parse', '--verify', 'refs/heads/' + branch).stdout.strip()
            if not existing.stdout.strip() and branch_head == head:
                require(git(root, 'branch', '--set-upstream-to=origin/' + branch, branch))
        else:
            print('本地跟踪引用有并发变化，已保留；远端上传已确认。')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['check', 'preflight', 'push'])
    parser.add_argument('--repo', default=os.getcwd())
    parser.add_argument('--approved-head', help='仅在已有明确上传授权时传入完整 SHA')
    parser.add_argument('--approved-remote', help='与已授权上传目标一致的完整 origin 推送地址')
    parser.add_argument('--approved-branch', help='与已授权上传目标一致的分支名')
    args = parser.parse_args()
    try:
        root, remote, slug, head, branch = context(args.repo)
        net = Network(root)
        old_sha = check(root, remote, slug, head, branch, net)
        if args.action != 'check':
            preflight(root, remote, head, branch, old_sha, net)
        if args.action == 'push':
            publish(root, remote, head, branch, net, args.approved_head,
                    args.approved_remote, args.approved_branch)
    except (Failure, ValueError, EOFError) as exc:
        print('\n未完成：' + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
