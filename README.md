![alt text](https://github.com/CHC-Computations/Harmonize/blob/main/logo-1.png?raw=true)

## SkosIt: Data Transformation and Enrichment Pipeline

![alt text](https://github.com/CHC-Computations/SkosIt/blob/main/SkosIt(1).png?raw=true)

### Overview
SkosIt is a specialized tool that aims to streamline the transformation and enrichment process of bibliographic data. The pipeline begins with raw tabular data in the [MARC21](https://www.loc.gov/marc/bibliographic/) bibliographic data format, augments this data using multiple external services, and finally converts it to SKOS-compliant RDF triples using Python's [rdflib](https://rdflib.readthedocs.io/en/stable/) library.

### Workflow

1. **Data Collection**: The initial dataset consists of tabular bibliographic records adhering to the MARC21 standard. This data serves as the foundation for the entire transformation process.

2. **Data Enrichment**: 
    - **[VIAF (Virtual International Authority File)](https://viaf.org/)**: The pipeline taps into the VIAF service to add authoritative information to the bibliographic records.
    - **[GeoNames](https://www.geonames.org/)**: Geographical metadata is pulled from GeoNames to enrich location-related fields in the records.
    - **[Wikidata](https://www.wikidata.org/)**: Additional general metadata and properties are collected from Wikidata.

3. **Data Transformation**: 
    - The enriched data is then processed using Python's [rdflib](https://rdflib.readthedocs.io/en/stable/) library, which allows for the generation of RDF triples.
    - The resulting triples are [SKOS (Simple Knowledge Organization System)](https://www.w3.org/TR/skos-reference/) compliant, making them interoperable and easy to integrate into semantic web applications.

### Technologies Used
- [MARC21 Data Format](https://www.loc.gov/marc/bibliographic/)
- [VIAF](https://viaf.org/)
- [GeoNames](https://www.geonames.org/)
- [Wikidata](https://www.wikidata.org/)
- [Python's rdflib library](https://rdflib.readthedocs.io/en/stable/)

By using SkosIt, you are equipping your dataset with rich, authoritative, and semantically interoperable metadata, primed for integration into a wide range of digital humanities projects.




![alt_text](https://github.com/CHC-Computations/Harmonize/blob/main/Zrzut%20ekranu%202022-12-19%20o%2017.48.49.png?raw=true)
