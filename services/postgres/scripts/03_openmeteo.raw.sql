CREATE TABLE IF NOT EXISTS raw.openmeteo_measurements (
	id				BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- clé technique
	latitude		DOUBLE PRECISION,
	longitude		DOUBLE PRECISION,
	measured_at		TIMESTAMPTZ NOT NULL,
	temperture_2m	DOUBLE PRECISION,
	precipitation	DOUBLE PRECISION,
	wind_speed_10m	DOUBLE PRECISION,
	source			TEXT		NOT NULL DEFAULT 'open-meteo',
	ingested_at		TIMESTAMPTZ NOT NULL DEFAULT now(),
	run_id			UUID,

-- contrainte qui rend l'UPSERT possible (clé d'idempotence, stratégie A)
	CONSTRAINT uq_openmeteo_point_time UNIQUE (latitude, longitude, measured_at)
);

-- Index pour que /weather/point soit rapide (filtre fréquent sur point + temps)
CREATE INDEX IF NOT EXISTS ix_openmeteo_point_time
	ON raw.openmeteo_measurements (latitude, longitude, measured_at);