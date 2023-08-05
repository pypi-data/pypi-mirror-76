# IMPORT PACKAGES
from cerebralcortex import Kernel
import numpy as np
import pandas as pd
from pyspark.sql.functions import pandas_udf, PandasUDFType
from pyspark.sql.types import StructField, StructType, IntegerType, TimestampType, StringType, FloatType

# CREATE CC OBJECT
CC = Kernel("/home/jupyter/cc3_conf/", study_name='rice')

# GET STREAM DATA FOR ONE USER
# md2k_aa_rice user_id = a57f8608-439a-4f11-9bbf-085ca01577f6
# rice user_id = 047dfad3-0807-37f0-bc90-7fd9dedb9bde
accel_ds = CC.get_stream("accelerometer--org.md2k.motionsense--motion_sense--right_wrist", user_id="047dfad3-0807-37f0-bc90-7fd9dedb9bde")

# Show 2 rows
accel_ds.show(2)

# This is the schema (column name and data type) that pandas udf should return. You can change types and column names to
# start experimenting with. These types and column names should match with the pandas DF return from pandas udf.
schema = StructType([
    StructField("timestamp", TimestampType()),
    StructField("localtime", TimestampType()),
    StructField("user", StringType()),
    StructField("version", IntegerType()),
    StructField("x", FloatType()),
    StructField("y", FloatType()),
    StructField("z", FloatType()),
    StructField("magnitude", FloatType()),
    StructField("activity", StringType())
])

# This is a sample pandas udf, input to this (sample_udaf) is pandas df and return type is pandas df
@pandas_udf(schema, PandasUDFType.GROUPED_MAP)
def sample_udaf(data):
    all_vals = []

    for index, row in data.iterrows():
        # NOTE: IF YOU ARE USING MD2K_AA_RICE STUDY THEN COLUMN NAMES ARE DIFFERENT, PLEASE UPDATE
        accelerometer_x = row["x"]
        accelerometer_y = row["y"]
        accelerometer_z = row["z"]

        x = np.array([accelerometer_x, accelerometer_y, accelerometer_z])
        magnitude = np.linalg.norm(x)
        if magnitude>0.21:
            activity = "active"
        else:
            activity = "stationary"
        all_vals.append([row["timestamp"],row["localtime"], row["user"],1,accelerometer_x, accelerometer_y, accelerometer_z, magnitude, activity])

    return pd.DataFrame(all_vals,columns=['timestamp','localtime', 'user', 'version','x','y','z','magnitude','activity'])

# Use CC built method to apply a pandas udf on the streamd data
result = accel_ds.compute(sample_udaf, windowDuration=10)

# show results
result.show(truncate=False)