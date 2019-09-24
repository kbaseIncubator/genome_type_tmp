/*
Workspace reference to a genome object.
@id kb
*/
typedef string Genome_id;

/*
External database reference from which this genome data originated.
Examples: "NC_014248"
@id external
*/
typedef string source_id;

/*
Publication data about this genome.
Fields:
    0: float  pubmedid
    1: string source (ex. Pubmed)
    2: string title
    3: string web address
    4: string publication year
    5: string authors
    6: string journal
*/
typedef tuple<float, string, string, string, string, string, string> publication;

/*
Workspace reference to an ontology object
@id ws KBaseOntology.OntologyDictionary
*/
typedef string Ontology_ref;

/*
TODO what is this
@optional ontology_ref method_version eco
*/
typedef structure {
  string id;
  Ontology_ref ontology_ref;
  string method;
  string method_version;
  string timestamp;
  string eco;
} Ontology_event;

/*
External database identifier for a coding sequence.
Example: "EPWB_RS00005_CDS_1"
@id external
*/
typedef string cds_id;

/*
External database identifier of a contiguous sequence within the genome.
Example: "NZ_LKAC01000001.1"
@id external
*/
typedef string Contig_id;

/*
Feature identifier (eg. the locus tag for a gene)
Example: "EPWB_RS00020"
@id external
*/
typedef string Feature_id;

/*
TODO what is this
@id external
*/
typedef string mrna_id;

/*
category;#Maybe a controlled vocabulary
    type;#Maybe a controlled vocabulary
*/
typedef structure {
  string category;
  string type;
  string evidence;
} InferenceInfo;

/*
Structure for a single feature CDS

      flags are flag fields in GenBank format. This will be a controlled vocabulary.
        Initially Acceptable values are pseudo, ribosomal_slippage, and trans_splicing
        Md5 is the md5 of dna_sequence.

        @optional parent_gene parent_mrna functions ontology_terms note flags warnings
        @optional inference_data dna_sequence aliases db_xrefs functional_descriptions
*/
typedef structure {
  cds_id id;
  list<tuple<Contig_id, int, string, int>> location;
  string md5;
  string protein_md5;
  Feature_id parent_gene;
  mrna_id parent_mrna;
  string note;
  list<string> functions;
  list<string> functional_descriptions;
  mapping<string, mapping<string, list<int>>> ontology_terms;
  list<string> flags;
  list<string> warnings;
  list<InferenceInfo> inference_data;
  string protein_translation;
  int protein_translation_length;
  list<tuple<string, string>> aliases;
  list<tuple<string, string>> db_xrefs;
  string dna_sequence;
  int dna_sequence_length;
} CDS;

/*
Structure for a single feature mRNA

      flags are flag fields in GenBank format. This will be a controlled vocabulary.
        Initially Acceptable values are pseudo, ribosomal_slippage, and trans_splicing
        Md5 is the md5 of dna_sequence.

        @optional parent_gene cds functions ontology_terms note flags warnings
        @optional inference_data dna_sequence aliases db_xrefs functional_descriptions
*/
typedef structure {
  mrna_id id;
  list<tuple<Contig_id, int, string, int>> location;
  string md5;
  Feature_id parent_gene;
  cds_id cds;
  string dna_sequence;
  int dna_sequence_length;
  string note;
  list<string> functions;
  list<string> functional_descriptions;
  mapping<string, mapping<string, list<int>>> ontology_terms;
  list<string> flags;
  list<string> warnings;
  list<InferenceInfo> inference_data;
  list<tuple<string, string>> aliases;
  list<tuple<string, string>> db_xrefs;
} mRNA;

/*
Reference to an Assembly object in the workspace
@id ws KBaseGenomeAnnotations.Assembly
*/
typedef string Assembly_ref;

/*
Reference to a taxon object
@id ws KBaseGenomeAnnotations.Taxon
*/
typedef string Taxon_ref;

/*
Reference to a handle to the Genbank file on shock
@id handle
*/
typedef string genbank_handle_ref;

/*
Reference to a handle to the GFF file on shock
@id handle
*/
typedef string gff_handle_ref;

/*
Reference to a report object
@id ws KBaseReport.Report
*/
typedef string Method_report_ref;

/*
Score_interpretation: fraction_complete - controlled vocabulary managed by API
@optional method_report_ref method_version
*/
typedef structure {
  string method;
  Method_report_ref method_report_ref;
  string method_version;
  string score;
  string score_interpretation;
  string timestamp;
} GenomeQualityScore;

typedef int Bool;

/*
Field descriptions:
    id: string object id
    scientific_name: human readable species name
    domain: human readable phylogenetic domain name
    warnings: list of string - warnings generated in the annotation process
    genome_tiers: list of string - TODO what is this
        Genome_tiers : controlled vocabulary (based on ap input and API checked)
        Allowed values: #Representative, Reference, ExternalDB, User
        Examples Tiers:
        All phytozome - Representative and ExternalDB
        Phytozome flagship genomes - Reference, Representative and ExternalDB
        Ensembl - Representative and ExternalDB
        RefSeq Reference - Reference, Representative and ExternalDB
        RefSeq Representative - Representative and ExternalDB
        RefSeq Latest or All Assemblies folder - ExternalDB
        User Data - User tagged
    feature_counts: map of string to integer - total counts of each type of feature TODO which
    genetic_code: An NCBI-assigned integer categorizing the organism: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi 
    dna_size: integer - total number of nucleotides
    num_contigs: integer - total number of contigs TODO flesh out
    molecule_type: string - DNA
    contig_lengths: list of int - nucleotide length of each contig in the genome
    contig_ids: list of str - identifiers of each contig TODO
    source: str - descriptor of where this data came from TODO
        TODO source_id or source??      Source: allowed entries RefSeq, Ensembl, Phytozome, RAST, Prokka, User_upload
        TODO should it be User or User_upload
    source_id: identifier of where this data came from TODO
    md5: string - content hash of the object's metadata TODO confirm
    taxonomy: string - semicolon-delimited taxonomy lineage from root node on the left to the strain or species on the right.
    taxon_assignments: mapping of taxonomy namespace to taxon ID.
        example: {"ncbi": "286", "gtdb": "s__staphylococcus_devriesei"}
    gc_content: float - ratio of GC count to AT in the genome
    publications: tuple of (pubmedid, source, title, web_addr, year, authors, journal). See typedef above.
    ontology_events: TODO
    ontologies_present: TODO
    features: TODO
    non_coding_features: TODO
    cdss: TODO
    mrnas: TODO
    assembly_ref: workspace reference to an assembly object from which this annotated genome was derived.
    taxon_ref: workspace reference to a taxon object that classifies the species or strain of this genome.
    genbank_handle_ref: file server handle reference to the source genbank file for this genome.
    gff_handle_ref: file server handle reference to the source GFF file for this genome.
    external_source_origination_date: TODO
    release: TODO
    original_source_file_name: filename from which this genome was derived (eg. genbank or gff filename).
    notes: TODO
    quality_scores: TODO
    suspect: bool - TODO
    genome_type: string - TODO

@optional warnings contig_lengths contig_ids source_id taxonomy publications
@optional ontology_events ontologies_present non_coding_features mrnas genome_type
@optional genbank_handle_ref gff_handle_ref external_source_origination_date
@optional release original_source_file_name notes quality_scores suspect assembly_ref
@optional taxon_ref

@metadata ws gc_content as GC content
@metadata ws taxonomy as Taxonomy
@metadata ws md5 as MD5
@metadata ws dna_size as Size
@metadata ws genetic_code as Genetic code
@metadata ws domain as Domain
@metadata ws source_id as Source ID
@metadata ws source as Source
@metadata ws scientific_name as Name
@metadata ws genome_type as Type
@metadata ws length(features) as Number of Protein Encoding Genes
@metadata ws length(cdss) as Number of CDS
@metadata ws assembly_ref as Assembly Object
@metadata ws num_contigs as Number contigs
@metadata ws length(warnings) as Number of Genome Level Warnings
@metadata ws suspect as Suspect Genome
*/
typedef structure {
  Genome_id id;
  string scientific_name;
  string domain;
  list<string> warnings;
  list<string> genome_tiers;
  mapping<string, int> feature_counts;
  int genetic_code;
  int dna_size;
  int num_contigs;
  string molecule_type;
  list<int> contig_lengths;
  list<string> contig_ids;
  string source;
  source_id source_id;
  string md5;
  string taxonomy;
  map<string, string> taxon_assignments;
  float gc_content;
  list<publication> publications;
  list<Ontology_event> ontology_events;
  mapping<string, mapping<string, string>> ontologies_present;
  list<Feature> features;
  list<NonCodingFeature> non_coding_features;
  list<CDS> cdss;
  list<mRNA> mrnas;
  Assembly_ref assembly_ref;
  Taxon_ref taxon_ref;
  genbank_handle_ref genbank_handle_ref;
  gff_handle_ref gff_handle_ref;
  string external_source_origination_date;
  string release;
  string original_source_file_name;
  string notes;
  list<GenomeQualityScore> quality_scores;
  Bool suspect;
  string genome_type;
} Genome;
