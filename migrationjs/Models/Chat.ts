import { type } from "os";
import { BaseEntity, Column, Entity, PrimaryColumn } from "typeorm";

@Entity()
export class Chat extends BaseEntity {

    @PrimaryColumn({
        type: "int8"
    })
    telegramId!: number

    @Column({
        default: false
    })
    isInGame!: boolean
}