# NLP Rag'a'Muffin

### I - Scraping de recettes de muffin

Afin de constituer une base de données pour notre RAG, il faut récupérer des recettes sur des sites de cuisine en français. 

J'ai d'abord essayé d'utiliser un package TypeScript ([Marmiton-api](https://sotrxii.github.io/marmiton-api/)) pour scraper les recettes du site Marmiton qui n'a pas fonctionné. J'ai laissé la version d'essai dans le folder `marmiton_scraping_api(not_working)`.

Dans un second temps, j'ai utilisé les packages python `beautiful-soup` et `recipe-scraper`,  respectivement afin de récupérer la liste des URL de pages de recettes de Muffin puis de récupérer le contenu de ces pages. Une fois lancé, le script `recipe_scraping.py` stocke les recettes de muffin au format JSON dans un folder `data/`.

### II - Embedding des recettes et constitution d'une base de donnée vectorielle Qdrant


### Crédits 

Music by @LATPaudio