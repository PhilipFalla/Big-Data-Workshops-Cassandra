-- Mini-reto G3 (Discord) - Philip Falla, 20240667
-- Una tabla por consulta. Los datos que en SQL venian de un JOIN se copian en cada tabla.

CREATE KEYSPACE IF NOT EXISTS discord_20240667
  WITH replication = {'class': 'NetworkTopologyStrategy', 'dc-g3': 3};

-- C1. Perfil de un usuario: se busca por usuario_id, una fila por usuario.
CREATE TABLE IF NOT EXISTS discord_20240667.usuarios_por_id (
  usuario_id     text,
  nombre_usuario text,
  creado_en      timestamp,
  PRIMARY KEY ((usuario_id))
);

-- C2. Los 20 mensajes mas recientes de un canal, con el autor.
-- usuario_id se guarda para poder actualizar nombre_usuario si el usuario lo cambia.
CREATE TABLE IF NOT EXISTS discord_20240667.mensajes_por_canal (
  canal_id       text,
  enviado_en     timestamp,
  mensaje_id     int,
  usuario_id     text,
  nombre_usuario text,
  contenido      text,
  PRIMARY KEY ((canal_id), enviado_en, mensaje_id)
) WITH CLUSTERING ORDER BY (enviado_en DESC, mensaje_id ASC);

-- C3. Los 10 mensajes mas recientes de un usuario, con el canal y el servidor.
-- canal_id se guarda para poder ubicar el mismo mensaje en mensajes_por_canal.
CREATE TABLE IF NOT EXISTS discord_20240667.mensajes_por_usuario (
  usuario_id      text,
  enviado_en      timestamp,
  mensaje_id      int,
  canal_id        text,
  nombre_canal    text,
  nombre_servidor text,
  contenido       text,
  PRIMARY KEY ((usuario_id), enviado_en, mensaje_id)
) WITH CLUSTERING ORDER BY (enviado_en DESC, mensaje_id ASC);

-- C4. Cuantos mensajes tuvo un canal en un dia (dia en UTC, calculado en la carga).
CREATE TABLE IF NOT EXISTS discord_20240667.mensajes_por_canal_dia (
  canal_id   text,
  dia        date,
  enviado_en timestamp,
  mensaje_id int,
  PRIMARY KEY ((canal_id, dia), enviado_en, mensaje_id)
);
