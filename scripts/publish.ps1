<#
.SYNOPSIS
  一键把个人档案仓库发布到 GitHub。

.DESCRIPTION
  依次执行：校验 -> 本地初始化与提交 -> 创建远端仓库 -> 推送 -> 设置描述。
  支持两种认证方式：
    1) 已安装 GitHub CLI 且 gh auth login 过（推荐）
    2) 设置环境变量 GITHUB_TOKEN（需 repo 权限）

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\publish.ps1 -Repo ai-profile -Visibility public

.EXAMPLE
  $env:GITHUB_TOKEN = "ghp_xxx"; .\scripts\publish.ps1 -Repo ai-profile
#>
[CmdletBinding()]
param(
    [string]$Repo = "ai-profile",
    [ValidateSet("public", "private")]
    [string]$Visibility = "public",
    [string]$Description = "AI 时代的个人档案：写给人和模型共读的自我说明",
    [string]$Branch = "main"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

function Info($m) { Write-Host $m -ForegroundColor Cyan }
function Good($m) { Write-Host "  v $m" -ForegroundColor Green }
function Warn2($m) { Write-Host "  ! $m" -ForegroundColor Yellow }
function Dead($m) {
    Write-Host ""
    Write-Host "x $m" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Dead "未找到 git。请先安装：winget install --id Git.Git -e （然后重开终端）"
}

Info "== 1/4 校验档案 =="
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python scripts\validate.py
    if ($LASTEXITCODE -ne 0) { Dead "校验未通过，先修复再发布。" }
    Good "校验通过"
}
else {
    Warn2 "未找到 python，跳过校验（建议之后补跑）"
}

Info "== 2/4 本地提交 =="
if (-not (Test-Path ".git")) {
    git init -b $Branch | Out-Null
    Good "已初始化 git 仓库（分支 $Branch）"
}
$uname = (git config user.name)
if (-not $uname) {
    git config user.name "Your Name"
    Warn2 "未配置 git 用户名，已临时设为 Your Name（之后可用 git commit --amend --reset-author 修正）"
}
$umail = (git config user.email)
if (-not $umail) {
    git config user.email "you@example.com"
    Warn2 "未配置 git 邮箱，已临时设为 you@example.com"
}
git add -A
$staged = (git status --porcelain)
if ($staged) {
    git commit -m "docs: 初始化 AI 时代个人档案" | Out-Null
    Good "已提交：$((git rev-parse --short HEAD))"
}
else {
    Warn2 "没有新的改动可提交"
}

Info "== 3/4 创建远端仓库 =="
$remote = (git remote get-url origin 2>$null)
if ($remote) {
    Good "已存在远端：$remote"
}
elseif (Get-Command gh -ErrorAction SilentlyContinue) {
    gh auth status *> $null
    if ($LASTEXITCODE -eq 0) {
        $visFlag = "--$Visibility"
        gh repo create $Repo $visFlag --source . --remote origin --push --description $Description
        if ($LASTEXITCODE -ne 0) { Dead "gh 创建仓库失败，请检查是否已有同名仓库。" }
        Good "已通过 gh 创建并推送"
    }
    else {
        Warn2 "gh 已安装但未登录，请先运行：gh auth login"
    }
}
elseif ($env:GITHUB_TOKEN) {
    $headers = @{
        Authorization          = "token $($env:GITHUB_TOKEN)"
        "User-Agent"           = "ai-profile-publisher"
        "Accept"               = "application/vnd.github+json"
    }
    $me = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
    $isPrivate = $false
    if ($Visibility -eq "private") { $isPrivate = $true }
    $body = @{
        name        = $Repo
        description = $Description
        private     = $isPrivate
    } | ConvertTo-Json
    Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $headers -Body $body -ContentType "application/json" | Out-Null
    git remote add origin "https://x-access-token:$($env:GITHUB_TOKEN)@github.com/$($me.login)/$Repo.git"
    git push -u origin $Branch
    git remote set-url origin "https://github.com/$($me.login)/$Repo.git"
    Good "已通过 GITHUB_TOKEN 创建并推送"
    Write-Host "  仓库地址：https://github.com/$($me.login)/$Repo"
}
else {
    Write-Host ""
    Write-Host "没有可用的 GitHub 认证，已停在本地提交阶段。" -ForegroundColor Yellow
    Write-Host "三选一后重新运行本脚本："
    Write-Host "  A) winget install --id GitHub.cli -e ; gh auth login"
    Write-Host "  B) `$env:GITHUB_TOKEN = 'ghp_xxx'  (GitHub Settings -> Developer settings -> Tokens)"
    Write-Host "  C) 网页手动建仓，然后："
    Write-Host "     git remote add origin https://github.com/<你的用户名>/$Repo.git"
    Write-Host "     git push -u origin $Branch"
    exit 0
}

Info "== 4/4 收尾 =="
Write-Host "  本地仓库：$root"
Write-Host "  下一步：在 GitHub 仓库页设置 About 描述、添加 topics（personal-profile / ai-native / llms-txt）"
Write-Host "  提醒：公开前确认已替换示例内容（搜索 yourname、example.com、林深）"
