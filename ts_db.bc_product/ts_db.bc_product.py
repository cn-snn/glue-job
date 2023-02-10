import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame


def directJDBCSource(
    glueContext,
    connectionName,
    connectionType,
    database,
    table,
    redshiftTmpDir,
    transformation_ctx,
) -> DynamicFrame:

    connection_options = {
        "useConnectionProperties": "true",
        "dbtable": table,
        "connectionName": connectionName,
    }

    if redshiftTmpDir:
        connection_options["redshiftTmpDir"] = redshiftTmpDir

    return glueContext.create_dynamic_frame.from_options(
        connection_type=connectionType,
        connection_options=connection_options,
        transformation_ctx=transformation_ctx,
    )


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node ts_db.bc_product
ts_dbbc_product_node1676022079932 = directJDBCSource(
    glueContext,
    connectionName="snn-aws-qadb-ts_db",
    connectionType="sqlserver",
    database="snn-aws-qadb.ci1zpybquepd.rds.cn-northwest-1.amazonaws.com.cn:1433;database=SNNTranSale",
    table="ts_db.bc_product",
    redshiftTmpDir="",
    transformation_ctx="ts_dbbc_product_node1676022079932",
)

# Script generated for node Amazon S3
AmazonS3_node1676020039525 = glueContext.write_dynamic_frame.from_options(
    frame=ts_dbbc_product_node1676022079932,
    connection_type="s3",
    format="csv",
    connection_options={
        "path": "s3://snn-dw1.0-storage/glue-cn-test/target/",
        "partitionKeys": [],
    },
    transformation_ctx="AmazonS3_node1676020039525",
)

job.commit()
