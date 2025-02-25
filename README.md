# Data Storage
# Background
Pacbook adalah sebuah perusahaan yang berfokus pada menjual beragam jenis buku. Peprusahaan Pacbook ingin memisahkan tempat penyimpanan data traksasi dan tempat penyimpanan untuk data analisa.

## Requirement Gathering dan Solution
Data yang telah dimiliki perlu untuk diolah lebih lanjut karena kedua data tersebut berada di dua tempat yang berbeda sehingga sulit untuk dilakukan analisa.

Solusi:
1. Membuat pipeline. Pipeline yang dibuat akan mengekstrak data dari kedua sumber data, kemudian melakukan transform pada data tersebut dan me-load data ke satu database sehingga lebih dapat digunakan untuk analisa.

2. Melakukan scheduling sehingga proses dilakukan secara berkala dan otomatis.

## Design dari Warehouse
Business Process:
- Taking Order

Grains:
- Sebuah data pembelian yang dilakukan oleh kustomer.
- Sebuah data pembelian buku setiap harinya.

Dimensions:
- dim_customer
- dim_book
- dim_date

Fact Table:
- fact_customer_order_daily
- fact_book_ordered_daily

#### Data Warehouse Diagram 

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image1.png)


## ETL Design
Pipeline akan mengikuti alur seperti pada gambar, yaitu:
- Extract
- Transform
- Load

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image2.png)


## ETL Scheduling 
Untuk memastikan bahwa pipeline dijalankan secara berkala maka dilakukan scheduling menggunakan crontab. 

Script yang akan dijalankan oleh crontab adalah sebagai berikut.

~~~
#!/bin/bash

echo "========== Start dbt with Luigi Orchestration Process =========="

# Set Python script
PYTHON_SCRIPT="./elt.py"

# Get Current Date
current_datetime=$(date '+%d-%m-%Y_%H-%M')

# Append Current Date in the Log File
LOG_FILE="./logs/elt/elt_$current_datetime.log"

echo "========== End of dbt with Luigi Orchestration Process =========="
~~~


# Testing Scenario
### Scenario 1
Initial Load

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image5.png)


Table dim_book

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image3.png)

Table dim_customer

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image4.png)

Table fact_cust_order_daily

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image6.png)


### Scenario 2
Update Data

![alt text](https://github.com/KyrieCettyara/Intro-to-data-ETL/blob/main/image/before_testing1.png)


### Scenario 3
Add New Data

Menambahkan data baru di source database

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image10.png)

Data sebelumnya belum ada di source database

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image11.png)

Data sebelumnya belum ada di schema data warehouse

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image11.png)


Data muncul di schema data warehouse

![alt text](https://github.com/KyrieCettyara/data-storage-project/blob/main/image/image14.png)





