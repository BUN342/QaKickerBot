import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from "typeorm";

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
    score!: number

}