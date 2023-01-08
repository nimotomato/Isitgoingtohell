CREATE TABLE public.news (
	id INT GENERATED ALWAYS AS IDENTITY,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	headline text NOT NULL,
	"date" TIMESTAMP NOT NULL,
	region text NOT NULL,
	source text NOT NULL,
	"label" text NOT NULL,
	score float8 NOT NULL,
	UNIQUE (headline)
);