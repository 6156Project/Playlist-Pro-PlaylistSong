create database if not exists PlaylistPro;
use PlaylistPro;

drop table if exists PlaylistPro.Song;
drop table if exists PlaylistPro.Playlist;
drop table if exists PlaylistPro.PlaylistSong;

create table PlaylistPro.Song (
    id varchar(36) primary key,
  	songName varchar(30),
    artist varchar(30)
);

create table PlaylistPro.Playlist (
  	id varchar(36) primary key,
  	playlistName varchar(50)
);

create table PlaylistPro.PlaylistSong (
	  songId varchar(36) not null,
  	playlistId varchar(36) not null,
  	foreign key (songId) references Song(id),
  	foreign key (playlistId) references Playlist(id) on delete cascade,
  	unique key (songId, playlistId)
);

insert into PlaylistPro.Song (id, songName, artist)
values("001", "Cinema", "Skrillex"),
      ("002", "WaterFall", "Disclosure"),
      ("003", "Dopamine", "Purple Disco Machine"),
      ("004", "Never Be Like You", "Flume"),
      ("005", "Hypnotized", "Purple Disco Machine")
;

insert into PlaylistPro.Playlist (id, playlistName)
values ("123", "Bangers");

insert into PlaylistPro.PlaylistSong(songId, playlistId)
values("001", "123"),
      ("002", "123"),
      ("003", "123"),
      ("004", "123"),
      ("005", "123");
      
      