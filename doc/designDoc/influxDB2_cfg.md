```
influx config create --config-name testCfg  --host-url http://localhost:8086 --org ncl --token 123123 --active
```

```
influx config create -n ycLocalCfg -u http://localhost:8086 -p admin:admin -o ncl
```

```
influx setup -u admin -p admin -o ncl -b BUCKET_NAME -f
```

problem: 

```
Error: instance has already been set up
```

solution: 

remove all the content in folder : C:\Users\liu_y\\.influxdbv2

username/password: admin/admin123