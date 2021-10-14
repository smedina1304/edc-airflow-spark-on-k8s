from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os

# aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
# aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']

# set conf - aws
# conf = (
# SparkConf()
#     .set("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
#     .set("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
#     .set("spark.hadoop.fs.s3a.fast.upload", True)
#     .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
#     .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.7.3')
# )

#gcp_sa_json = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

# set conf - gcp
conf = (
SparkConf()
    .set("fs.gs.impl","com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    .set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
    .set("fs.gs.auth.service.account.enable", "true")
#    .set("fs.gs.auth.service.account.json.keyfile", gcp_sa_json)
)

# apply config
sc = SparkContext(conf=conf).getOrCreate()
    

if __name__ == "__main__":

    print('*****************')
    print('Iniciando SparkSession')
    print('*****************')

    # init spark session
    spark = SparkSession\
            .builder\
            .appName("Repartition Job")\
            .getOrCreate()

    #spark.sparkContext.setLogLevel("WARN")

    print('*****************')
    print('Lendo titanic.csv')
    print('*****************')

    df = (
        spark
        .read
        .format('csv')
        .options(header='true', inferSchema='true', delimiter=',')
        .load('gs://dl-techinical-apps/samples/titanic/raw/titanic.csv')
    )
    

    df.show()
    df.printSchema()

    print('*****************')
    print('Gravando parquet')
    print('*****************')    

    (df
    .write
    .mode('overwrite')
    .format('parquet')
    .save('gs://dl-techinical-apps/samples/titanic/processing/titanic.csv')
    )

    print('*****************')
    print('Escrito com sucesso!')
    print('*****************')

    spark.stop()