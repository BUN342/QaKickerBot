import { BaseEntity, Column, Entity, JoinTable, ManyToMany, PrimaryGeneratedColumn } from "typeorm";
import { Match } from "./Match";

@Entity()
export class User extends BaseEntity {

    @PrimaryGeneratedColumn()
    id!: number

    @Column()
    telegram_id!: number

    @Column()
    name!: string

    @Column({nullable: true,
    default: 0})
    score?: number

    @Column({
        default: false
    })
    isInMatch!: boolean

    @ManyToMany(() => Match)
    @JoinTable()
    matches?: Match[]

}