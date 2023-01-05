CREATE TABLE public.news (
	id INT GENERATED ALWAYS AS IDENTITY, 
	headline text NOT NULL,
	"date" DATE NOT NULL,
	region text NOT NULL,
	scraped_at DATE NOT NULL,
	"label" text NOT NULL,
	score float8 NOT NULL,
	UNIQUE (headline)
);