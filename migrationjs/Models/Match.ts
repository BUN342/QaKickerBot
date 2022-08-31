import { BaseEntity, Column, Entity, PrimaryGeneratedColumn } from "typeorm";

@Entity()
export class Match extends BaseEntity {

    @PrimaryGeneratedColumn()
    id!: number

    @Column({
        nullable: true
    })
    score_win?: number

    @Column({
        nullable: true
    })
    score_lose?: string

}