BEGIN;

CREATE SCHEMA IF NOT EXISTS relego;

create table if not exists relego.set
(
    id           integer not null
        primary key,
    name         text    not null,
    description  text,
    released     integer not null,
    theme        text    not null,
    parts_volume integer not null
);

create unique index if not exists set__name__unique_idx
    on set (name);

create table if not exists relego.part
(
    id     integer not null,
    set_id integer not null
        references set
            on delete cascade,
    volume integer not null,
    color  text    not null
);

create index if not exists part__id_volume_color_idx
    on part (id, volume, color);

create table if not exists relego.user_data
(
    login    text not null,
    password text not null,
    set_ids  integer[]
);

create unique index if not exists user_data__login__unique_idx
    on user_data (login);

COMMIT;