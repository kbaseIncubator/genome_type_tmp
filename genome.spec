/*
KBase legacy data ID
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
    1: string source (eg. "Pubmed")
    2: string title
    3: string URL of publication
    4: string publication year
    5: string authors (eg. "Smith,K., Doe,N., Chan,Y.")
    6: string journal
*/
typedef tuple<float, string, string, string, string, string, string> publication;

/*
Workspace reference to an ontology object
@id ws KBaseOntology.OntologyDictionary
*/
typedef string Ontology_ref;

/*
An ontology event is a record of the service and method used for a set of
ontology assignments on the genome.
Fields:
  id - name of the ontology (eg. "GO", "ENVO")
  ontology_ref - workspace reference to the ontology source object
  method - method from the service that created the ontology for a given source
  method_version - version of the above method
  timestamp - epoch of when this assignment occured
  eco - TODO
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
Identifier of an mRNA sequence
@id external
*/
typedef string mrna_id;

/*
TODO
Found in the `inference_data` fields in mRNAs and CDSs

Fields
  category: string - TODO
  type: string - TODO
  evidence: string - TODO
*/
typedef structure {
  string category;
  string type;
  string evidence;
} InferenceInfo;

/*
Structure for a single coding sequence.

Coding sequences are the sections of a feature's sequence that are translated
to a protein (minus introns and UTRs).

Fields:
  id: string - identifier of the coding sequence, such as "b0001_CDS_1"
  location: list of (string, int, string, int) - list of locations from where
      this sequence originates in the original assembly. Each sub-sequence in the
      list constitutes a section of the resulting CDS. The first element in
      the tuple corresponds to the "contig_id", such as "NC_000913.3". The second
      element in the tuple is an index in the contig of where the sequence starts.
      The third element is either a plus or minus sign indicating whether it is
      on the 5' to 3' leading strand ("+") or on the 3' to 5' lagging strand
      ("-"). The last element is the length of the sub-sequence.
      For a location on the leading strand (denoted by "+"), the index is of
      the leftmost base, and the sequence extends to the right.
      For a location on the lagging strand (denoted by "-"), the index is of
      the rightmost base, and the sequence extends to the left.
      NOTE: the last element in each tuple is the *length* of each
      sub-sequence. If you have a location such as ("xyz", 100, "+", 50), then
      your sequence will go from index 100 to index 149 (this has a length of
      50). It *does not* go from index 100 to index 150, as that would have a
      length of 51.
      Likewise, if you have the location ("xyz", 100, "-", 50), then the
      sequence extends from 100 down to 51, which has a length of 50 bases. It
      does not go from index 100 to 50, as that would have a length of 51.
  md5: string - md5 of the dna sequence - TODO clarification
  protein_md5: string - hash of the protein sequence that this CDS encodes
  parent_gene: string - gene (feature) from which this CDS comes from,
      including introns and UTRs that have been removed to create this CDS.
  parent_mrna: string - mRNA sequence from which this sequence is derived,
      including UTRs but not introns.
  note: string - TODO
  functions: list of string - list of protein products or chemical
      processes that this sequence creates, facilitates, or influences.
  functional_descriptions: list of string - TODO list of protein products or chemical
      processes that sequence creates, facilitates, or influences.
  ontology_terms: map of string to (map of string to (list of int)) - a mapping
      of ontology source id (eg. "GO") to a mapping of term IDs (eg "GO:16209") to
      a list of indexes into the ontology_events data (found in the top level
      of the genome object). The index into an ontology event indicates what
      service and method created this term assignment.
  flags: list of string - controlled vocab - fields from the genbank source. A
      common example is "pseudo" for pseudo-genes that do not encode proteins,
      which shows up as "/pseudo" in the genbank.
      Values can be: "pseudo", "ribosomal_slippage", "trans_splicing"
  warnings: list of string - TODO
  inference_data: list of InferenceInfo - TODO
  protein_translation: string - amino acid sequence that this CDS gets translated into.
  protein_translation_length: int - length of the above
  aliases: list of (string, string) - alternative list of names or identifiers
      eg: [["gene", "thrA"], ["locus_tag", "b0002"]]
  db_xrefs: list of (string, string) - Identifiers from other databases (database cross-references)
      The first string is the database name, the second is the database identifier.
      eg: [["ASAP", "ABE-0000006"], ["EcoGene", "EG11277"]]
  dna_sequence: string - sequence of exons from the genome that constitute this protein encoding sequence.
  dna_sequence_length: int - length of the above

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
The mRNA is the transcribed sequence from the original feature, minus the
introns, but including the UTRs.

Fields:
  id: string - identifying string for the mRNA
  location: list of (string, int, string, int) - list of locations from where
      this sequence originates in the original assembly. Each sub-sequence in the
      list constitutes a section of the resulting CDS. The first element in
      the tuple corresponds to the "contig_id", such as "NC_000913.3". The second
      element in the tuple is an index in the contig of where the sequence starts.
      The third element is either a plus or minus sign indicating whether it is
      on the 5' to 3' leading strand ("+") or on the 3' to 5' lagging strand
      ("-"). The last element is the length of the sub-sequence.
      For a location on the leading strand (denoted by "+"), the index is of
      the leftmost base, and the sequence extends to the right.
      For a location on the lagging strand (denoted by "-"), the index is of
      the rightmost base, and the sequence extends to the left.
      NOTE: the last element in each tuple is the *length* of each
      sub-sequence. If you have a location such as ("xyz", 100, "+", 50), then
      your sequence will go from index 100 to index 149 (this has a length of
      50). It *does not* go from index 100 to index 150, as that would have a
      length of 51.
      Likewise, if you have the location ("xyz", 100, "-", 50), then the
      sequence extends from 100 down to 51, which has a length of 50 bases. It
      does not go from index 100 to 50, as that would have a length of 51.
  md5: string - md5 of the dna sequence - TODO clarification
  parent_gene: Feature_id - corresponding feature for this sequence, including introns and UTRs
  cds: string - corresponding coding sequence for this mRNA (the sequence minus UTRs)
  dna_sequence: string - sequence of UTRs and exons from the genome that constitute this mRNA
  dna_sequence_length: int - length of the above
  note: string - TODO
  functions: list of string - TODO list of protein products or chemical
      processes that sequence creates, facilitates, or influences.
  functional_descriptions: list of string - TODO list of protein products or chemical
      processes that sequence creates, facilitates, or influences.
  ontology_terms: map of string to (map of string to (list of int)) - a mapping
      of ontology source id (eg. "GO") to a mapping of term IDs (eg "GO:16209") to
      a list of indexes into the ontology_events data (found in the top level
      of the genome object). The index into an ontology event indicates what
      service and method created this term assignment.
  flags: list of string - controlled vocab - fields from the genbank source. A
      common example is "pseudo" for pseudo-genes that do not encode proteins,
      which shows up as "/pseudo" in the genbank.
      Values can be: "pseudo", "ribosomal_slippage", "trans_splicing"
  warnings: list of string - TODO
  inference_data: list of InferenceInfo - TODO
  aliases: list of (string, string) - alternative list of names or identifiers
      eg: [["gene", "thrA"], ["locus_tag", "b0002"]]
  db_xrefs: list of (string, string) - Identifiers from other databases (database cross-references).
      The first string is the database name, the second is the database identifier.
      eg: [["ASAP", "ABE-0000006"], ["EcoGene", "EG11277"]]

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
Genome quality score

Fields:
  method: string -
  method_report_ref: string -
  method_version: string -
  score: string -
  score_interpretation: string -
  timestamp: string -

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
    id: string - KBase legacy data ID
    scientific_name: string - human readable species name
    domain: string - human readable phylogenetic domain name (eg. "Bacteria")
    warnings: list of string - genome-level warnings generated in the annotation process
    genome_tiers: list of string - controlled vocabulary (based on app input and checked by GenomeFileUtil)
        A list of labels describing the data source for this genome.
        Allowed values: Representative, Reference, ExternalDB, User
        Tier assignments based on genome source:
         * All phytozome - Representative and ExternalDB
         * Phytozome flagship genomes - Reference, Representative and ExternalDB
         * Ensembl - Representative and ExternalDB
         * RefSeq Reference - Reference, Representative and ExternalDB
         * RefSeq Representative - Representative and ExternalDB
         * RefSeq Latest or All Assemblies folder - ExternalDB
         * User Data - User tagged
    feature_counts: map of string to integer - total counts of each type of feature
        keys are a controlled vocabulary of: "CDS", "gene", "misc_feature",
        "misc_recomb", "mobile_element", "ncRNA": 72, "non_coding_features",
        "non_coding_genes", "protein_encoding_gene", "rRNA", "rep_origin",
        "repeat_region", "tRNA"
    genetic_code: int - An NCBI-assigned taxonomic category for the organism
        See here: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi
    dna_size: integer - total number of nucleotides
    num_contigs: integer - total number of contigs in the genome
    molecule_type: string - controlled vocab - the type of molecule sequenced
        Possible values are "Unknown", "DNA", "RNA", "genomic DNA", "genomic RNA",
        "mRNA", "tRNA", "rRNA", "other RNA", "other DNA", "transcribed RNA",
        "viral cRNA", "unassigned DNA", "unassigned RNA"
    contig_lengths: list of int - nucleotide length of each contig in the genome
        Indexes in this list correspond to indexes in the `contig_ids` list.
    contig_ids: list of str - external database identifiers for each contig (eg. "NC_000913.3")
    source: str - controlled vocab - descriptor of where this data came from (eg. "RefSeq")
        Allowed entries RefSeq, Ensembl, Phytozome, RAST, Prokka, User_upload
    source_id: string - identifier of this genome from the source database (eg. the RefSeq ID such as "NC_000913")
    md5: string - checksum of the underlying assembly sequence
    taxonomy: string - semicolon-delimited taxonomy lineage, in order of parent to child
    taxon_assignments: mapping of taxonomy namespace to taxon ID.
        example: {"ncbi": "286", "gtdb": "s__staphylococcus_devriesei"}
    gc_content: float - ratio of GC count to AT in the genome
    publications: tuple of (pubmedid, source, title, web_addr, year, authors, journal). See typedef above.
    ontology_events: A record of the service and method used for a set of
        ontology assignments on the genome.
    ontologies_present: a mapping of ontology source id (eg. "GO") to a mapping
        of term IDs (eg "GO:16209") to term names (eg. "histidine biosynthetic process").
    features: array of Feature - protein coding genes (see the separate Feature spec)
    cdss: array of protein-coding sequences
    mrnas: array of transcribed messenger RNA sequences (equal to cdss plus 5' and 3' UTRs)
    non_coding_features: array of features that does not include mRNA, CDS, and protein-encoding genes
    assembly_ref: workspace reference to an assembly object from which this annotated genome was derived.
    taxon_ref: workspace reference to a taxon object that classifies the species or strain of this genome.
    genbank_handle_ref: file server handle reference to the source genbank file for this genome.
    gff_handle_ref: file server handle reference to the source GFF file for this genome.
    external_source_origination_date: TODO look at GFU for this
    release: string - User-supplied release or version of the source data. This
        most likely will come from an input field in the import app.
    original_source_file_name: filename from which this genome was derived (eg. genbank or gff filename).
    notes: TODO
    quality_scores: TODO
    suspect: bool - flag of whether this annotation is problematic due to some warning
    genome_type: string - controlled vocab - One of "draft isolate",
        "finished isolate", "mag", "sag", "virus", "plasmid", "construct"

Features vs. coding sequences: a feature is a sequence in the DNA that codes
for a protein, including non-transcribed introns. A coding sequence (stored as
`cdss`) includes **only** the sections of the feature that codes for a protein,
minus introns and UTRs.

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
  mapping<string, string> taxon_assignments;
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
