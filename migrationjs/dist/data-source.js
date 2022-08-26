"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppDataSource = void 0;
const typeorm_1 = require("typeorm");
const User_1 = require("./Models/User");
require("reflect-metadata");
exports.AppDataSource = new typeorm_1.DataSource({
    type: "postgres",
    host: "ec2-34-242-8-97.eu-west-1.compute.amazonaws.com",
    port: 5432,
    username: "mdriysdmzxohga",
    password: "d5016c9242569d17b84950f4d0cb9ba3be135fbdff7d89e09f96785d5845e9a2",
    database: "dbf5g5orv48dsr",
    synchronize: true,
    logging: false,
    entities: [User_1.User],
    subscribers: [],
    migrations: [],
    schema: "testjs",
    extra: {
        ssl: {
            "rejectUnauthorized": false
        }
    }
});
exports.AppDataSource.initialize()
    .catch((error) => console.log(error));
