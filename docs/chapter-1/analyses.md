---
comments: true
---

# Analyses

Saat kita melakukan analisis, seringkali tidak untuk digunakan sebagai model dan tidak perlu dibuatkan tabelnya. Analysis hanya perlu di-compile untuk mendapatkan SQL query yang kemudian digunakan di BI tools untuk visualisasi.

Analisis dibuat dengan menggunakan SQL file biasa, namun ditaruh dalam folder `analyses`, misalnya `analyses/running_total_by_account.sql`. Hasil kompilasi file SQL-nya bisa ditemukan di `target/compiled/{project name}/analyses/running_total_by_account.sql`.

Kapan menggunakan analyses?

Mengetik dan meng-compile di dbt merupakan hal yang merepotkan, apalagi perlu mencari di mana file hasil compile-nya. Penggunaannya yang memudahkan adalah untuk mencari tahu dengan lengkap alamat dari sebuah model (database, schema, dan nama tabelnya) saat kita lupa. Misalnya `{{ ref('quickbooks_adjusted_journal_entries') }}` menjadi `dbt.finance.adjusted_journal`.

Jika tidak menggunakan analyses, kita perlu mencari alamat lengkap hasil pemrosesan dengan langkah-langkah di bawah ini. Cukup merepotkan kalau belum hafal.

Cara mengetahui alamat lengkap hasil materialisasi model:
- database-nya di mana, dengan melihat
  - `<project>.outputs.<target>.database` di `profiles.yml`, atau
  - di level model di `dbt_project.yml` di `models.<project>.<folder>.+database`.
- schema-nya di mana, caranya sama dengan database (lihat poin sebelumnya), dan
- tabel-nya di mana, dengan melihat
  - nama model di `models.name` di yaml model, yang sama dengan nama file sql model-nya,
  - value `alias` di `models.alias` di yaml model
  - melihat apakah ada macro `generate_alias_name`, misal seperti di bawah ini. Jika ada macro dengan nama tersebut, dbt akan otomatis memanggilnya untuk mendapatkan nama alias secara programatik.

```sql
{% macro generate_alias_name(custom_alias, node) -%}
    {# If an alias is defined in schema.yml, use it #}
    {% if custom_alias is not none %}
        {{ custom_alias }}
    {% else %}
        {# Otherwise, add a "dbt_" prefix to the model name #}
        dbt_{{ node.name }}
    {% endif %}
{%- endmacro %}
```