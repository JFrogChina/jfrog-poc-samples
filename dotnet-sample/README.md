# project-example

## Add dependency
dotnet add package Newtonsoft.Json --version 13.0.3

It will add an entry in .csproj
<PackageReference Include="Newtonsoft.Json" Version="13.0.3" />


## Add Artifactory as remote repository
 nuget sources Add -Name Artifactory -Source https://art-server/artifactory/api/nuget/v3/alex-nuget/index.json -username user -password pwd

Check the source has been added

nuget sources

## Download dependency
 dotnet restore


## Build package
dotnet pack


## Upload to Artifactory

 nuget push bin\Release\MyProject.1.0.0.nupkg -Source Artifactory