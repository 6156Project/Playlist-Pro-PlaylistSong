create database if not exists PlaylistSongs;
use PlaylistSongs;

drop table if exists PlaylistSongs.playlistsongs;

create table PlaylistSongs.playlistsongs (
	playlist_id varchar(39) not null,
  	song_id varchar(36) not null,
  	foreign key (song_id) references Song.songs(song_id),
  	foreign key (playlist_id) references Playlist.playlists(id) on delete cascade,
  	unique key (song_id, playlist_id)
);