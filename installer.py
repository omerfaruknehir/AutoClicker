import requests


def lstrepo(user, repo, branch="main"):
    repo = requests.get(
        f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    ).json()
    return repo['sha'], repo['tree']

def lstrelase(user, repo, branch="main"):
    repo = requests.get(
        f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    ).json()
    return repo['sha'], repo['tree']

def getfile(user, repo, path, branch='main'):
    bytes = requests.get(
        f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
    ).content
    return bytes

code, tree = lstrepo("OFN01", "AutoClicker")
print(code)
for file in tree:
    fl = getfile("OFN01", "AutoClicker", file['path'])
    print(fl)

{
    "sha": "280ea23fc79ebb91e97242a18621aa599f511c55",
    "url": "https://api.github.com/repos/OFN01/AutoClicker/git/trees/280ea23fc79ebb91e97242a18621aa599f511c55",
    "tree": [
        {
            "path": ".conf",
            "mode": "100644",
            "type": "blob",
            "sha": "2edeafb09db0093bae6ff060e2dcd2166f5c9387",
            "size": 2,
            "url": "https://api.github.com/repos/OFN01/AutoClicker/git/blobs/2edeafb09db0093bae6ff060e2dcd2166f5c9387",
        },
        {
            "path": "LICENSE",
            "mode": "100644",
            "type": "blob",
            "sha": "f288702d2fa16d3cdf0035b15a9fcbc552cd88e7",
            "size": 35149,
            "url": "https://api.github.com/repos/OFN01/AutoClicker/git/blobs/f288702d2fa16d3cdf0035b15a9fcbc552cd88e7",
        },
        {
            "path": "README.md",
            "mode": "100644",
            "type": "blob",
            "sha": "cdf64aa243ec7484c4f3f498810c6652f84d017e",
            "size": 487,
            "url": "https://api.github.com/repos/OFN01/AutoClicker/git/blobs/cdf64aa243ec7484c4f3f498810c6652f84d017e",
        },
        {
            "path": "app.py",
            "mode": "100644",
            "type": "blob",
            "sha": "3cd69faf462eead3557e59346649466c204981fe",
            "size": 11762,
            "url": "https://api.github.com/repos/OFN01/AutoClicker/git/blobs/3cd69faf462eead3557e59346649466c204981fe",
        },
        {
            "path": "icon.ico",
            "mode": "100644",
            "type": "blob",
            "sha": "195e8d9e7fab2094965616939a465ae1a4fbd1c4",
            "size": 268350,
            "url": "https://api.github.com/repos/OFN01/AutoClicker/git/blobs/195e8d9e7fab2094965616939a465ae1a4fbd1c4",
        },
    ],
    "truncated": False,
}
