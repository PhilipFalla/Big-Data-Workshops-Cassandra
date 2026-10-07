-- C1. Perfil de un usuario.
SELECT usuario_id, nombre_usuario, creado_en
FROM discord_20240667.usuarios_por_id
WHERE usuario_id = 'du230';

-- C2. Los 20 mensajes mas recientes de un canal, con el autor.
SELECT enviado_en, nombre_usuario, contenido
FROM discord_20240667.mensajes_por_canal
WHERE canal_id = 'ch16'
LIMIT 20;

-- C3. Los 10 mensajes mas recientes de un usuario, con el canal y el servidor.
SELECT enviado_en, nombre_servidor, nombre_canal, contenido
FROM discord_20240667.mensajes_por_usuario
WHERE usuario_id = 'du186'
LIMIT 10;

-- C4. Cuantos mensajes tuvo un canal en un dia.
SELECT COUNT(*) AS mensajes
FROM discord_20240667.mensajes_por_canal_dia
WHERE canal_id = 'ch16' AND dia = '2026-09-04';
