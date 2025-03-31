---
title: "Cheatsheet"
description: "Mendefinisikan sumber data di dbt dengan menggunakan Source."
---

# Source

Source[^1] adalah bahan mentah pemrosesan yang berasal dari sumber data, dipanggil dalam SQL dengan menggunakan `{{source('nama_source', 'nama_table')}}`

<div class="grid cards" markdown>

- :fontawesome-brands-html5: __HTML__ for content and structure
- :fontawesome-brands-js: __JavaScript__ for interactivity
- :fontawesome-brands-css3: __CSS__ for text running out of boxes
- :fontawesome-brands-internet-explorer: __Internet Explorer__ ... huh?

</div>

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`mkdocs-material`](#) with [`pip`](#) and get up
    and running in minutes

    [:octicons-arrow-right-24: Getting started](#)

-   :fontawesome-brands-markdown:{ .lg .middle } __It's just Markdown__

    ---

    Focus on your content and generate a responsive and searchable static site

    [:octicons-arrow-right-24: Reference](#)

-   :material-format-font:{ .lg .middle } __Made to measure__

    ---

    Change the colors, fonts, language, icons, logo and more with a few lines

    [:octicons-arrow-right-24: Customization](#)

-   :material-scale-balance:{ .lg .middle } __Open Source, MIT__

    ---

    Material for MkDocs is licensed under MIT and available on [GitHub]

    [:octicons-arrow-right-24: License](#)

</div>

=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

| Method      | Description                          |
| :---------- | :----------------------------------- |
| `GET`       | :material-check:     Fetch resource  |
| `PUT`       | :material-check-all: Update resource |
| `DELETE`    | :material-close:     Delete resource |

![Image title](https://dummyimage.com/600x400/){ width="300", loading=lazy }
/// caption
Image caption
///

[Hover me](https://example.com "I'm a tooltip!")

The HTML specification is maintained by the W3C.

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! tip

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! question

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! warning

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! quote

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.


Misal kita buat file dalam folder `model/<filename>.yml` dengan isi sebagai berikut.
```yaml title="model/filename.yml" hl_lines="2 3"
sources:
  - name: jaffle_shop
    database: raw  
    schema: jaffle_shop  # (1)
    tables:
      - name: orders
```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

++ctrl+alt+del++



``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```

Artinya kita bisa memanggil table `raw.orders` dengan `#!sql+jinja {{ source('jaffle_shop', 'orders')}}`.

Tips: Sources bisa dikumpulkan di satu folder `model/sources/*_sources.yml`
Tips: Sources bisa dinamakan `sources.yml` jika hanya satu source, atau `<sesuatu>_sources.yml`. Akan lebih baik jika bisa membedakan dari sistem mana data ini diambil dari namanya.
Tips: Supaya tidak bingung dengan alias source, sebaiknya nama source dinamakan dengan `<database>_<schema>`, misal pada contoh di atas menjadi `raw_jaffle_shop`
Counter Tips: Tapi gimana kalau sumbernya ganti table saja? Seharusnya namanya lebih generic sehingga modular.
Counter Counter Tips: Kalau sumbernya ganti table likely ganti schema juga jadi bakal perlu tetep berubah.
Tips: description diisi oleh engineer somewhere lalu integrated ke sini somehow
Tips: wrap source dengan menggunakan sql query supaya kalau ada perubahan source bisa dihandle di sini. Caranya bikin model yang isinya cuma `SELECT * FROM source()`.

## Identifier

Kalau nama tablenya aneh, kita bisa pakai `identifier` sebagai nama table asli, dan `name` sebagai alias
```yaml
sources:
  - name: jaffle_shop
    database: raw  
    schema: jaffle_shop  
    tables:
      - name: orders # nama yang kita pengen
        identifier: nama_asli_tabel_yang_aneh
```

## Quoting

Dalam beberapa kasus, query ke database mewajibkan kita untuk menambahkan _quote_ di dalam query. Contohnya di Snowflake, nama table yang berasal dari reserved words perlu ditambahkan _quote_. Caranya adalah sebagai berikut.

```yaml
sources:
  - name: jaffle_shop
    database: raw
    quoting:
      database: true
      schema: true
      identifier: true

    tables:
      - name: order # perlu diquote karena order adalah reserved words
      - name: order_items
        # This overrides the `jaffle_shop` quoting config
        quoting:
          identifier: false
```

## Testing
Source bisa kita cek apakah ada masalah atau tidak dengan kualitas datanya, misal di bawah ini dites apakah id-nya unique dan tidak null.

```yaml
sources:
  - name: jaffle_shop
    description: This is a replica of the Postgres database used by our app
    tables:
      - name: orders
        description: >
          One record per order. Includes cancelled and deleted orders.
        columns:
          - name: id
            description: Primary key of the orders table
            tests:
              - unique
              - not_null
          - name: status
            description: Note that the status can change over time
```
Test semua source
```bash
dbt test --select "source:*"
```
Tes spesifik table
```bash
dbt test --select source:jaffle_shop.orders
```

## Running
Saat ada data dari sumber yang bermasalah, biasanya kita ingin menjalankan ulang semua pemrosesan yang terkait sumber tersebut. Caranya adalah menggunakan suffix `+`. Misal
```bash
dbt run --select source:jaffle_shop.orders+
```

## Freshness
Saat memproses data, tentu kita perlu mengecek apakah data yang kita akan proses sudah up-to-date atau belum. Misalkan kita memproses 100 sources, jika satu saja source out-dated, kita perlu memperoses ulang semuanya dan ini akan sangat costly. Maka dari itu, kita bisa menggunakan freshness. Deklarasi freshness menggunakan keyword `freshness` untuk konfigurasi seberapa sensitif terhadap ketertinggalan, dan `loaded_at_field` sebagai patokan kolom apa yang digunakan untuk mengecek waktu dibandingkan dengan waktu saat dijalankan. Freshness dapat dideklarasikan di level database maupun table. Contoh di bawah ini adalah deklarasi freshness di level table dengan `_etl_loaded_at` sebagai kolom untuk mengecek waktu.

```yaml
sources:
  - name: jaffle_shop
    database: raw
    tables:
      - name: orders
        freshness: # make this a little more strict
          warn_after: {count: 6, period: hour}
          error_after: {count: 12, period: hour}
          filter: "status = 'completed'"
        loaded_at_field: _etl_loaded_at
```

Dengan deklarasi di atas, saat kita menjalankan `dbt source freshness` atau `dbt source freshness --select source:jaffle_shop` misalnya, kita akan mendapatkan status fresheness untuk masing-masing table. Bisa dilihat juga bahwa kita bisa menggunakan `filter` untuk memilih kondisi apa yang akan digunakan saat mengecek freshness, dalam contoh di atas hanya yang statusnya `completed` saja. Jika ada table yang mau dikecualikan dari freshness, bisa dideklarasikan `freshness: null`.

Lalu hasilnya bisa kita gunakan pada command build seperti berikut, misalnya untuk memproses ulang data yang lulus freshness check.
```bash
dbt build --select source_status:fresher+
```

Hasil dari freshneess ini disimpan di `target/sources.json` dan bisa dibaca dengan menggunakan script misalnya dengan membaca json dengan python `sources[0].status == 'pass'`.

```json
{
  "metadata": {
    "generated_at": "2025-03-29T12:00:00Z",
    "dbt_version": "1.7.0"
  },
  "sources": [
    {
      "source_name": "my_source",
      "table_name": "my_table",
      "max_loaded_at": "2025-03-29T08:00:00Z",
      "snapshotted_at": "2025-03-29T12:00:00Z",
      "status": "pass",
      "max_loaded_at_time_ago_in_s": 14400  # (4 hours ago)
    }
  ]
}
```

[^1]:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.