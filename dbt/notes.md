# Notes for my team
- nggak ada description di source
- jalanin freshness, tapi ga ada yang pake freshness, dan hasilnya juga ga jelas dipake apa
- kita bisa define project lain sebagai package, instead of re-declare the model. E.g. everpro depend ke evermos. Contoh dependensi project dengan git di dalam `packages.yml` atau `dependencies.yml` di level yang sama dengan yaml project:
```yaml
packages:
  - git: "git@github.com:dbt-labs/dbt-utils.git" # git SSH URL
    revision: 0.9.2 # branch name, tag release, commit hash (full)
    subdirectory: "materialized-views" # name of subdirectory containing `dbt_project.yml`
```
Atau mengakses folder lain:
```yaml
packages:
  - local: relative/path/to/subdirectory
```