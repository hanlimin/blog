function Get-GitDate($file) {
    git log  --pretty=format:'%cd'  --date=format:'%Y-%m-%d %H:%M:%S' $file
}
function Get-CreateDate($file) {
    Get-GitDate $file | Select-Object -Last 1
}
function Get-ModifyDate($file) {
    Get-GitDate $file | Select-Object -First 1
}

Push-Location

Set-Location ..

# 
# 1. 添加YAML头部 ---
# 2. 添加date，使用git最新提交时间，没有则使用当前时间
# 3. 添加draft标识
# 4. 添加title，使用文件名
# 5. 添加type，使用文件夹名称
# 6. 添加lang，使用zh-CN
# 
Get-ChildItem  .\content -Filter *.md -Recurse | ForEach-Object -Process {
    $content = Get-Content $_.FullName
    $title = $_.BaseName
    $createDate = Get-CreateDate($_.FullName)
    $modifyDate = Get-ModifyDate($_.FullName)
    
    Set-Content -Path $_.FullName -Value "---`ntitle: $title`ndate: `"$createDate`"`nmodifyDate: `"$modifyDate`"`ndraft: true`n---`ns"
    Add-Content -Path $_.FullName -Value $content

}

Pop-Location
