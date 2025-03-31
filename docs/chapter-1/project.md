# Project

Project adalah satuan paling tinggi dalam dbt, ditandai dengan sebuah folder dan sebuah yaml configuration didalamnya `project.yml`.
- Satu project tidak bisa berhubungan dengan project yang lain, modelnya tidak bisa direferensikan.
- Satu project hanya bisa terhubung dengan satu database

Kapan pisah project?
- Kalau data dan transformasinya sensitif dan perlu pisah repo, manajemen akses dan security
- beda team (arguably masih oke satu project beda tim di beda folder)
- beda schedule (arguably masih bisa pakai select utk beda schedule)
- beda database, misal satu dbt ada di postgres lalu dilanjutkan di snowflake
- beda ritme development, misal jika mau rollback dan salah satu domain terlalu aktif, jadi sulit rollbacknya (alasan terkuat untuk beda tim beda project)

## Layering
- source
- staging, hanya refer ke source, tugasnya join2 data
- warehouse, hanya refer ke staging
- mart, hanya refer ke warehouse

