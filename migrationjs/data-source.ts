import { DataSource } from "typeorm";
import { User } from "./Models/User";
import "reflect-metadata"

export const AppDataSource = new DataSource({
    type: "postgres",
    host: "ec2-34-242-8-97.eu-west-1.compute.amazonaws.com",
    port: 5432,
    username: "mdriysdmzxohga",
    password: "d5016c9242569d17b84950f4d0cb9ba3be135fbdff7d89e09f96785d5845e9a2",
    database: "dbf5g5orv48dsr",
    synchronize: true,
    logging: false,
    entities: [User],
    subscribers: [],
    migrations: [],
    schema: "testjs",
    extra: {
        ssl: {
            "rejectUnauthorized": false
        }
    }
})

AppDataSource.initialize()
    .catch((error) => console.log(error))
