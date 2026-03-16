# BibTeX Format Reference

## Key Naming Convention

Format: `AuthorYearKeyword`

- **Author**: First author's surname only
- **Year**: 4-digit publication year
- **Keyword**: First significant word from title (skip "The", "A", "An", "On")

Examples: `Wardle2025Evolving`, `FernandezPichel2025Evaluating`, `Sun2024TrustingSearch`

Special cases: Hyphenated surnames → remove hyphen; Accents → remove; "et al." → first author only; Duplicate keys → append lowercase letter (e.g., `Author2024Keywordb`)

## Formatting Rules

1. **Indentation**: Single tab per field
2. **Titles**: Double braces `{{Title Here}}`
3. **Authors**: `Lastname, Firstname` separated by ` and `
4. **Month**: 3-letter lowercase (jan, feb, mar, etc.)
5. **DOI**: Without "https://doi.org/" prefix
6. **Trailing comma**: After last field value
7. **Entry spacing**: Blank line between entries

## URL Field Priority

1. **DOI URL**: If DOI available, use `https://doi.org/{DOI}`
2. **Other URL**: Only if confident (publisher page, stable repository)
3. **Omit**: If no reliable URL available

Note: `doi` field = DOI number only; `url` field = full DOI URL.

## Entry Type Examples

### @article

```bibtex
@article{Wardle2025Evolving,
	title = {{Evolving Health Information–Seeking Behavior in the Context of Google AI Overviews, ChatGPT, and Alexa: Interview Study Using the Think-Aloud Protocol}},
	volume = {27},
	url = {https://doi.org/10.2196/79961},
	doi = {10.2196/79961},
	number = {1},
	urldate = {2025-10-14},
	journal = {Journal of Medical Internet Research},
	author = {Wardle, Claire and Urbani, Shaydanay and Wang, Eric},
	month = oct,
	year = {2025},
	pages = {e79961},
}
```

### @inproceedings

```bibtex
@inproceedings{Vladika2024HealthFC,
	title = {{HealthFC: Verifying Health Claims with Evidence-Based Medical Fact-Checking}},
	url = {https://aclanthology.org/2024.lrec-main.709/},
	urldate = {2025-10-09},
	booktitle = {{Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024)}},
	publisher = {ELRA and ICCL},
	author = {Vladika, Juraj and Schneider, Phillip and Matthes, Florian},
	editor = {Calzolari, Nicoletta and Kan, Min-Yen and Hoste, Veronique and Lenci, Alessandro and Sakti, Sakriani and Xue, Nianwen},
	month = may,
	year = {2024},
	pages = {8095--8107},
}
```

With address and series:

```bibtex
@inproceedings{Jin2024BetterEnglish,
	address = {New York, NY, USA},
	series = {{WWW '24}},
	title = {{Better to Ask in English: Cross-Lingual Evaluation of Large Language Models for Healthcare Queries}},
	url = {https://doi.org/10.1145/3589334.3645643},
	doi = {10.1145/3589334.3645643},
	urldate = {2025-09-21},
	booktitle = {Proceedings of the {ACM} {Web} {Conference} 2024},
	publisher = {Association for Computing Machinery},
	author = {Jin, Yiqiao and Chandra, Mohit and Verma, Gaurav and Hu, Yibo and De Choudhury, Munmun and Kumar, Srijan},
	month = may,
	year = {2024},
	pages = {2627--2638},
}
```

### @misc (Preprints, arXiv)

**arXiv papers**: Use `howpublished = {arXiv [Preprint]}` (not `publisher` or `note`).

```bibtex
@misc{Sun2024TrustingSearch,
	title = {{Trusting the Search: Unraveling Human Trust in Health Information from Google and ChatGPT}},
	author = {Sun, Xin and Ma, Rongjun and Zhao, Xiaochang and Li, Zhuying and Lindqvist, Janne and Ali, Abdallah El and Bosch, Jos A.},
	url = {https://doi.org/10.48550/arXiv.2403.09987},
	doi = {10.48550/arXiv.2403.09987},
	urldate = {2025-10-01},
	howpublished = {arXiv [Preprint]},
	month = mar,
	year = {2024},
}
```

### @book

```bibtex
@book{AuthorYearKeyword,
	title = {{Book Title Here}},
	author = {Lastname, Firstname and Lastname2, Firstname2},
	publisher = {Publisher Name},
	address = {City, Country},
	year = {2024},
	isbn = {978-0-000-00000-0},
	url = {https://doi.org/10.xxxx/xxxxx},
}
```

### @techreport

```bibtex
@techreport{AuthorYearKeyword,
	title = {{Technical Report Title}},
	author = {Lastname, Firstname},
	institution = {Institution Name},
	type = {Technical Report},
	number = {TR-2024-001},
	year = {2024},
	url = {https://example.com/report.pdf},
	month = jan,
}
```

### @phdthesis

```bibtex
@phdthesis{AuthorYearKeyword,
	title = {{Dissertation Title}},
	author = {Lastname, Firstname},
	school = {University Name},
	year = {2024},
	type = {PhD Thesis},
	address = {City, Country},
}
```

## Fields Reference Table

| Field | article | inproceedings | misc | book | techreport | phdthesis |
|-------|---------|---------------|------|------|------------|-----------|
| title | Required | Required | Required | Required | Required | Required |
| author | Required | Required | Required | Required | Required | Required |
| year | Required | Required | Required | Required | Required | Required |
| journal | Required | - | - | - | - | - |
| booktitle | - | Required | - | - | - | - |
| publisher | - | Recommended | - | Required | - | - |
| school | - | - | - | - | - | Required |
| institution | - | - | - | - | Required | - |
| volume | Recommended | - | - | - | - | - |
| number | Optional | - | - | - | Optional | - |
| pages | Recommended | Recommended | - | - | - | - |
| doi | Recommended | Recommended | Recommended | Optional | Optional | Optional |
| url | Recommended | Recommended | Recommended | Optional | Recommended | Optional |
| howpublished | - | - | Recommended | - | - | - |
| month | Recommended | Recommended | Optional | - | Optional | - |
| address | - | Optional | - | Optional | - | Optional |
| editor | - | Optional | - | - | - | - |

## Determining Entry Type from PDF

| Indicators | Type |
|------------|------|
| Volume/issue numbers, journal name | @article |
| "Proceedings of", conference acronym | @inproceedings |
| arxiv.org URL, "preprint" | @misc |
| Organizational/government report | @techreport |
| ISBN, book publisher | @book |
| Dissertation, university submission | @phdthesis |

## Special Characters

**In BibTeX keys**: Remove accents (é→e, ñ→n) and hyphens.

**In field values**: Preserve accents; escape LaTeX special chars (& → \&, % → \%).
