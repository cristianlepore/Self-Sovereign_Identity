from owlready2 import *
from rdflib.namespace import RDF
from rdflib import Graph, URIRef
from rdflib.namespace import XSD
from rdflib.plugins.sparql.processor import SPARQLResult

# === CONFIGURATION ===
OWL_FILE_PATH = "eIDAS.owl"
TECH_LAYER1_NS = "http://example.org/techLayer1#"


# === LOAD ONTOLOGY AND APPLY REASONING ===
try:
    ontology = get_ontology(f"file://{OWL_FILE_PATH}").load()
except Exception as e:
    print(f"Error to load the ontology: {e}")
    exit(1)

with ontology:
    sync_reasoner(infer_property_values=True)

# === EXTRACT INFERRED RDF GRAPH ===
rdf_graph: Graph = ontology.world.as_rdflib_graph()




# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1
# Users must have unrestricted access to their own information.
#
#

query_holder_has_data_vault = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?h a techLayer1:Holder .
  ?h techLayer1:agencyOfUserAgent ?ua .
  ?ua a techLayer1:UserAgent .
  ?ua techLayer1:hasDataVault ?dv .
  ?dv a techLayer1:DataVault .
}}
"""

condition1 = bool(rdf_graph.query(query_holder_has_data_vault).askAnswer)



#
# Condition 2
# Users must have unrestricted access to the list of identity and service providers.
#
#

# Controlla se Issuer è registrato
query_issuer_registered = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>
ASK {{
  ?iss a techLayer1:Issuer .
  ?iss techLayer1:issuerRegisteredInRegistry ?rg .
  ?rg a ?class .
  ?class rdfs:subClassOf* techLayer1:Registry .

  # ?reg a techLayer1:Registrar .
  # ?reg techLayer1:registersIssuer ?iss .
}}
"""

issuer_registered = bool(rdf_graph.query(query_issuer_registered).askAnswer)

# Controlla se Verifier è registrato
query_verifier_registered = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>
ASK {{
  ?ver a techLayer1:Verifier .
  ?ver techLayer1:verifierRegisteredInRegistry ?rg .
  ?rg a ?class .
  ?class rdfs:subClassOf* techLayer1:Registry .

  # ?reg a techLayer1:Registrant .
  # ?reg techLayer1:registersVerifier ?ver .
}}
"""

verifier_registered = bool(rdf_graph.query(query_verifier_registered).askAnswer)

if issuer_registered:
# --- Controllo 1: Issuer è registrato e il registro coincide con l'AuthoritativeSource ---
    query_issuer_ok = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK {{
        ?h a techLayer1:Holder .
        ?h techLayer1:holderConsultsAuthoritativeSource ?as .
        ?as a techLayer1:AuthoritativeSource .
 
        ?iss a techLayer1:Issuer .
        ?iss techLayer1:issuerRegisteredInRegistry ?as .
        ?as a techLayer1:AuthoritativeSource .
    }}
    """

if verifier_registered:
# --- Controllo 2: Verifier è registrato e il registro coincide con l'AuthoritativeSource ---
    query_verifier_ok = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>
    ASK {{
        ?h a techLayer1:Holder .
        ?h techLayer1:holderConsultsAuthoritativeSource ?as .
        ?as a techLayer1:AuthoritativeSource .
  
        ?vr a techLayer1:Verifier .
        ?vr techLayer1:verifierRegisteredInRegistry ?as .
        ?as a techLayer1:AuthoritativeSource .
    }}
    """

# Esegui le query solo se i rispettivi registri esistono
issuer_ok = bool(rdf_graph.query(query_issuer_ok).askAnswer) if issuer_registered else False
verifier_ok = bool(rdf_graph.query(query_verifier_ok).askAnswer) if verifier_registered else False

if not issuer_registered and not verifier_registered:
    # Controlla se Holder non consulta nulla
    query_no_consult = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>
    ASK {{
      ?h a techLayer1:Holder .
      ?h techLayer1:holderConsultsAuthoritativeSource ?as .
      ?as a techLayer1:AuthoritativeSource .    
    }}
    """

# Se issuer o verifier non sono registrati, non c'è consulto
query_no_consult = None

# === LOGICA FINALE ===

if issuer_registered and verifier_registered:
    condition2 = issuer_ok and verifier_ok
    if condition2:
        condition2 = 1.0
    elif issuer_ok and not verifier_ok:
        condition2 = 0.5
    elif not issuer_ok and verifier_ok:
        condition2 = 0.5
    else:
        condition2 = 0.0
elif issuer_registered:
    condition2 = issuer_ok
    if condition2:
        condition2 = 1.0
    else:
        condition2 = 0.0
elif verifier_registered:
    condition2 = verifier_ok
    if condition2:
        condition2 = 1.0
    else:
        condition2 = 0.0
else:
    condition2 = query_no_consult



#
# Condition 3
# They should be able to retrieve every piece of information that constitutes their identity, including claims and assertions.
#
#

# Eseguiamo la query sul DataVault (sempre)
data_vault_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>
SELECT (COUNT(DISTINCT ?cr_dv) AS ?numCredentialsInDV) (COUNT(DISTINCT ?cr_total) AS ?totalCredentials)
WHERE {{
  {{
    ?h a techLayer1:Holder .
    ?h techLayer1:agencyOfUserAgent ?ua .
    ?ua a techLayer1:UserAgent .
    ?ua techLayer1:hasDataVault ?dv .
    ?dv a techLayer1:DataVault .
    ?dv techLayer1:maintainsCredential ?cr_dv .
    ?cr_dv a ?class .
    ?class rdfs:subClassOf* techLayer1:Credential .
  }}
  UNION
  {{
    ?cr_total a ?class2 .
    ?class2 rdfs:subClassOf* techLayer1:Credential .
  }}
}}
"""

try:
    results = rdf_graph.query(data_vault_query)
    num_credentials_in_dv = 0
    total_credentials = 0
    for row in results:
        num_credentials_in_dv = int(row.numCredentialsInDV)
        total_credentials = int(row.totalCredentials)

    condition3 = num_credentials_in_dv / total_credentials if total_credentials > 0 else 0.0
except Exception as e:
    print(f"Errore nella query Condition 3: {e}")
    condition3 = False  # In caso di errore, consideriamo il risultato falso



#
# Condition 4
# They should be able to retrieve every piece of information that constitutes their identity, including claims and assertions.
#
#

# Query per verificare se esiste un AuthoritativeSource che memorizza una Credential
stores_credential_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>
ASK {{
    {{
        ?tr a ?class .
        ?class rdfs:subClassOf* techLayer1:TrustRegistry .
        ?tr techLayer1:storesCredential ?cr . 
        ?cr a ?classCr .
        ?classCr rdfs:subClassOf* techLayer1:Credential .
    }}
    UNION
    {{
        ?as a ?class2 .
        ?class2 rdfs:subClassOf* techLayer1:AuthoritativeSource .
        ?as techLayer1:storesCredential ?cr2 . 
        ?cr2 a ?classCr2 .
        ?classCr2 rdfs:subClassOf* techLayer1:Credential .
    }}
}}
"""

# Prova a eseguire la prima query, gestendo possibili eccezioni
try:
    stores_credential_result = rdf_graph.query(stores_credential_query).askAnswer
except Exception:
    stores_credential_result = None  # In caso di errore, consideriamo None

# Inizializziamo authoritative_query_result come False
authoritative_query_result = False

# Se la prima query ha restituito True, eseguiamo anche la query sull'holder
if stores_credential_result is True:
    try:
        stored_cr_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>
        SELECT (COUNT(DISTINCT ?cr) AS ?storedCrCount)
        WHERE {{
            {{
                ?tr a ?class .
                ?class rdfs:subClassOf* techLayer1:TrustRegistry .
                
                ?tr techLayer1:storesCredential ?cr .
                ?cr a ?class2 .
                ?class2 rdfs:subClassOf* techLayer1:Credential .
            }}
            UNION
            {{
                ?h a techLayer1:Holder .
                ?h techLayer1:holderConsultsAuthoritativeSource ?as .
                ?as a ?class3 .
                ?class3 rdfs:subClassOf* techLayer1:AuthoritativeSource .
                ?as techLayer1:storesCredential ?cr .
                ?cr a ?class4 .
                ?class4 rdfs:subClassOf* techLayer1:Credential .
            }}
        }}
        """

        total_cr_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>
        SELECT (COUNT(DISTINCT ?cr) AS ?totalCrCount)
        WHERE {{
            ?cr a ?class .
            ?class rdfs:subClassOf* techLayer1:Credential .
        }}
        """

        stored_result = rdf_graph.query(stored_cr_query)
        total_result = rdf_graph.query(total_cr_query)

        stored_count = int([row.storedCrCount.toPython() for row in stored_result][0])
        total_count = int([row.totalCrCount.toPython() for row in total_result][0])

        condition4 = (stored_count / total_count) if total_count > 0 else 0
    except Exception as e:
        print(f"Errore durante l'esecuzione delle query: {e}")

# Calcolo finale di condition3 in base alla logica specificata
if stores_credential_result is False:
    # Ignora authoritative_query_result
    condition4 = None



#
# Condition 5
# This access must be granted without discrimination based on [ethnicity, gender, socio-economic status, language, or ]geographic location.
#
#

query_has_admin = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>
ASK {{
  ?aa a ?classAa .
  ?classAa rdfs:subClassOf* techLayer1:AdministeringAuthority .
}}
"""

query_has_gov = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>
ASK {{
  ?gv a ?classGv .
  ?classGv rdfs:subClassOf* techLayer1:GoverningAuthority .
}}
"""

has_admin = bool(rdf_graph.query(query_has_admin).askAnswer)
has_gov = bool(rdf_graph.query(query_has_gov).askAnswer)


if has_admin:
    query_admin_part = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK {{
      {{
        ?aa a ?classAa .
        ?classAa rdfs:subClassOf* techLayer1:AdministeringAuthority .

        ?aa techLayer1:administersDigitalTrustUtility ?rg .
        ?rg a ?classRg .
        ?classRg rdfs:subClassOf* techLayer1:DigitalTrustUtility .

        ?rg techLayer1:resolvesRegistry ?rg2 .
        ?rg2 a ?classRg2 .
        ?classRg2 rdfs:subClassOf* techLayer1:DigitalTrustUtility .

        ?aa2 techLayer1:administersDigitalTrustUtility ?rg2 .
        ?aa2 a ?classAa2 .
        ?classAa2 rdfs:subClassOf* techLayer1:AdministeringAuthority .
      }}
    }}
    """
    admin_part = rdf_graph.query(query_admin_part).askAnswer

if has_gov:
    query_gov_part = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK {{
      {{
        ?gv a ?classGv .
        ?classGv rdfs:subClassOf* techLayer1:GoverningAuthority .

        ?gv techLayer1:governsRegistry ?rg .
        ?rg a ?class .
        ?class rdfs:subClassOf* techLayer1:Registry .

        ?rg techLayer1:resolvesRegistry ?rg2 .
        ?rg2 a ?class2 .
        ?class2 rdfs:subClassOf* techLayer1:Registry .

        ?gv2 techLayer1:governsRegistry ?rg2 .
        ?gv2 a ?classGv2 .
        ?classGv2 rdfs:subClassOf* techLayer1:GoverningAuthority .
      }}
    }}
    """
    gov_part = rdf_graph.query(query_gov_part).askAnswer

if has_admin and has_gov:
    condition5 = admin_part and gov_part
    if condition5:
        condition5 = 1.0
    else:
        condition5 = 0.0
elif has_admin:
    condition5 = admin_part
    if condition5:
        condition5 = 1.0
    else:
        condition5 = 0.0
elif has_gov:
    condition5 = gov_part
    if condition5:
        condition5 = 1.0
    else:
        condition5 = 0.0
else:
    condition5 = None



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Access': {
        'group': 'Usability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3,
            'Condition 4': condition4,
            'condition 5': condition5
        }
    }
}

result_condition = {}
result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================



#
# Condition 1:
# A self-sovereign identity must guarantee complete autonomy in managing [and administering ]identity information.
#
#

autonomy = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
    ?h a techLayer1:Holder .
    ?h techLayer1:agencyOfUserAgent ?ua .
    ?ua a techLayer1:UserAgent .
    ?ua techLayer1:hasKeyManagementSystem ?kms .
    ?kms a techLayer1:KeyManagementSystem .
}}
"""

condition1 = rdf_graph.query(autonomy).askAnswer



#
# Condition 2:
# A self-sovereign identity must guarantee complete autonomy in [managing and ]administering identity information.
#
#

# 1. Query SPARQL per contare tutte le Digital Trust Utility
total_dt_query = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(DISTINCT ?dt) AS ?totalDT)
WHERE {{
    ?dt a ?dtType .
    ?dtType rdfs:subClassOf* techLayer1:Identifier .
}}
"""

# 2. Query SPARQL per contare, per ogni AdministeringAuthority, quante DT amministra
per_aa_query = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT ?aa (COUNT(DISTINCT ?dt) AS ?countDT)
WHERE {{
    ?aa a techLayer1:AdministeringAuthority .
    ?aa techLayer1:administersDigitalTrustUtility ?dt .
    ?dt a ?dtType .
    ?dtType rdfs:subClassOf* techLayer1:Identifier .
}}
GROUP BY ?aa
"""

# 3. Esegui le query
total_dt_result = rdf_graph.query(total_dt_query)
per_aa_result = rdf_graph.query(per_aa_query)

# 4. Estrai il numero totale di DT
total_dt = 0
for row in total_dt_result:
    total_dt = int(row.totalDT)

# Evita divisione per zero
if total_dt == 0:
    max_percentage = 0.0
else:
    # 5. Calcola le percentuali per ciascun ?aa
    percentages = [
        int(row.countDT) / total_dt
        for row in per_aa_result
    ]
    max_percentage = max(percentages) if percentages else 0.0

condition2 = max_percentage



#
# Condition 3:
# Users should have full autonomy over the creation of their identity.
#
#

autonomy = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?h a techLayer1:Holder .
  ?h techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:ProofPresentationProtocol .
  ?ttp techLayer1:presentationProof ?pr .
  ?pr a ?class .
  ?class rdfs:subClassOf* techLayer1:Proof .

  FILTER NOT EXISTS {{
    ?iss a techLayer1:Issuer .
    ?iss techLayer1:usesTrustTaskProtocol ?ttp .
    ?ttp a techLayer1:ProofPresentationProtocol .
    ?ttp techLayer1:presentationProof ?pr .
  }}

  FILTER NOT EXISTS {{
    ?vr a techLayer1:Verifier .
    ?vr techLayer1:usesTrustTaskProtocol ?ttp .
    ?ttp a techLayer1:ProofPresentationProtocol .
    ?ttp techLayer1:presentationProof ?pr .
  }}  
}}
"""

condition3 = rdf_graph.query(autonomy).askAnswer



#
# Condition 4:
# Users bear sole responsibility for all related operations, without dependence on any third party.
#
#

autonomy = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?h a techLayer1:Holder .
  ?h techLayer1:agencyOfUserAgent ?ua .
  ?ua a techLayer1:UserAgent .
  ?ua techLayer1:enablesTSP ?tcp .
  ?tcp a techLayer1:TrustedCommunicationProtocol .

  FILTER NOT EXISTS {{
    ?tcp techLayer1:routesThroughIntermediarySystem ?interm .
    ?interm a ?intermClass .
    ?intermClass rdfs:subClassOf* techLayer1:IntermediarySystem .
  }}
}}
"""

condition4 = rdf_graph.query(autonomy).askAnswer



#
# Condition 5:
# Users bear sole responsibility for all related operations, without dependence on any third party.
#
#

# === CONDIZIONE 5 ===
# Calcola la proporzione di identificatori decentralizzati supportati da una architettura decentralizzata

prefix = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>"""

# Trova tutti gli identificatori (inclusi quelli delle sottoclassi)
query_total_ids = f"""{prefix}
SELECT DISTINCT ?id WHERE {{
  ?id a ?class .
  ?class rdfs:subClassOf* techLayer1:Identifier .
}}
"""
total_ids = set(rdf_graph.query(query_total_ids))

# Trova tutti gli identificatori decentralizzati
query_decentralized_ids = f"""{prefix}
SELECT DISTINCT ?id WHERE {{
  ?id a ?class .
  ?class rdfs:subClassOf* techLayer1:DecentralizedIdentifier .
}}
"""
decentralized_ids = set(rdf_graph.query(query_decentralized_ids))

# Trova quelli supportati da architettura decentralizzata
query_supported_ids = f"""{prefix}
SELECT DISTINCT ?id WHERE {{
  ?arch a techLayer1:DecentralizedArchitecture .
  ?arch techLayer1:supportsDecentralizedIdentifier ?id .
  ?id a ?class .
  ?class rdfs:subClassOf* techLayer1:DecentralizedIdentifier .
}}
"""
supported_ids = set(rdf_graph.query(query_supported_ids))

# Calcolo valore normalizzato
total_count = len(total_ids)
supported_count = len(supported_ids)

condition5 = supported_count / total_count if total_count > 0 else 0.0



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Autonomy': {
        'group': 'Usability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,      
            'Condition 3': condition3,
            'Condition 4': condition4,
            'Condition 5': condition5
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================



#
# Condition 1:
# Users must explicitly consent to the collection, use, and sharing of their personal data with a third party.
#
#

query_ask_holder_with_consent_format = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  {{
    ?h a techLayer1:Holder .
    ?h techLayer1:executesTrustApplication ?ta .
  }}
  UNION
  {{
    ?pr a techLayer1:Principal .
    ?pr techLayer1:executesTrustApplication ?ta .
  }}

  ?ta a techLayer1:TrustApplication .
  ?ta techLayer1:performsTrustTask ?tt .
  ?tt a techLayer1:TrustTask .
  ?tt techLayer1:includesConsent "true"^^xsd:boolean .
}}
"""

condition1 = rdf_graph.query(query_ask_holder_with_consent_format).askAnswer



#
# Condition 2:
# Furthermore, they should have the ability to withdraw their consent at any time.
#
#

# Se condition1 è True, esegui la query per condition2
if condition1:
    query_ask_holder_for_revocation = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?h a techLayer1:Holder .
  ?h techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:RevocationNotificationProtocol .
  techLayer1:RevocationNotificationProtocol rdfs:subClassOf techLayer1:TrustTaskProtocol .
  }}
"""
    condition2 = rdf_graph.query(query_ask_holder_for_revocation).askAnswer
else:
    condition2 = None



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Consent': {
        'group': 'Controllability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1:
# Users must have full control over their digital identity and attributes, serving as the ultimate authority over their own identity. This has led to the emergence of digital agents, like digital wallets, which serve as gatekeepers to a user's digital life.
#
#

control = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?h a techLayer1:Holder .
  ?h techLayer1:agencyOfUserAgent ?ua .
  ?ua a techLayer1:UserAgent .
  ?ua techLayer1:hasDataVault ?dv .
  ?dv a techLayer1:DataVault .
  ?dv techLayer1:maintainsCredential ?cr .

  ?cr a ?class .
  ?class rdfs:subClassOf* techLayer1:Credential .
  ?cr techLayer1:encodesAttribute ?attr .

  ?dv techLayer1:storesIdentifier ?id .
  ?id a ?class2 .
  ?class2 rdfs:subClassOf* techLayer1:Identifier .
}}
"""

condition1 = rdf_graph.query(control).askAnswer



#
# Condition 2:
# These tools allow users to manage their attributes in a unified manner while retaining full sovereignty over their identity.
#
#

control = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (?linkedCredentials / ?totalCredentials AS ?credentialRatio)
       (?linkedAttributes / ?totalAttributes AS ?attributeRatio)
WHERE {{

  {{
    SELECT (COUNT(DISTINCT ?cr) AS ?linkedCredentials)
    WHERE {{
      ?dv a techLayer1:DataVault .
      ?dv techLayer1:maintainsCredential ?cr .
      ?cr a ?class .
      ?class rdfs:subClassOf* techLayer1:Credential .
    }}
  }}

  {{
    SELECT (COUNT(DISTINCT ?cr_all) AS ?totalCredentials)
    WHERE {{
      ?cr_all a ?class_all .
      ?class_all rdfs:subClassOf* techLayer1:Credential .
    }}
  }}

  {{
    SELECT (COUNT(DISTINCT ?attr) AS ?linkedAttributes)
    WHERE {{
      ?cr a ?classCr .
      ?classCr rdfs:subClassOf* techLayer1:Credential .
      ?cr techLayer1:encodesAttribute ?attr .
      ?attr a techLayer1:Attribute .
    }}
  }}

  {{
    SELECT (COUNT(DISTINCT ?attr_all) AS ?totalAttributes)
    WHERE {{
      ?attr_all a techLayer1:Attribute .
    }}
  }}
}}
"""

results = rdf_graph.query(control)

for row in results:
    credential_ratio = float(row.credentialRatio)

condition2 = credential_ratio



#
# Condition 3:
# Users should always be able to [access, ]update, or conceal their identity as they see fit.
#
#

control = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?id a ?class .
  ?class rdfs:subClassOf* techLayer1:Identifier .

  ?id techLayer1:identifiesEntity ?h .
  ?h a techLayer1:Holder .

  ?id techLayer1:rotatesIdentifier ?id2 .
  ?id2 a ?class .
  ?class rdfs:subClassOf* techLayer1:Identifier .

  ?id2 techLayer1:identifiesEntity ?h .
}}
"""

condition3 = rdf_graph.query(control).askAnswer



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Control': {
        'group': 'Controllability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================



#
# Condition 1:
# [The creation, management, and adoption of a self-sovereign identity must not involve hidden costs, licensing fees, or any other financial charges for simply owning an identity.] Costs for service provides must be kept to a minimum, ensuring that the benefits of SSI outweigh the expenses.
#
#

cost_entities = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT ?countRg ?countAgent ?countEnt
WHERE {{
  {{
    SELECT (COUNT(?rg) AS ?countRg)
    WHERE {{
      ?rg a ?clsRg .
      ?clsRg rdfs:subClassOf* techLayer1:Registry .
    }}
  }}
  {{
    SELECT (COUNT(?ua) AS ?countAgent)
    WHERE {{
      ?ua a techLayer1:UserAgent .
    }}
  }}
  {{
    SELECT (COUNT(?ent) AS ?countEnt)
    WHERE {{
      ?ent a ?cls .
      ?cls rdfs:subClassOf* techLayer1:Entity .

      # FILTER NOT EXISTS {{
      #   ?ent a techLayer1:Holder .
      # }}
    }}
  }}
}}
"""

# Esegui la query
result = rdf_graph.query(cost_entities)

# Estrai i valori
for row in result:
    count_rg = int(row.countRg)
    count_agent = int(row.countAgent)
    count_ent = int(row.countEnt)
    total_count = count_rg + count_agent + count_ent

query_class_counts = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT ?countClsRg ?countClsAgent ?countClsEnt
WHERE {{
  {{
    SELECT (COUNT(DISTINCT ?clsRg) AS ?countClsRg)
    WHERE {{
      ?rg a ?clsRg .
      ?clsRg rdfs:subClassOf* techLayer1:Registry .
    }}
  }}
  {{
    SELECT (COUNT(DISTINCT ?clsAgent) AS ?countClsAgent)
    WHERE {{
      ?ua a ?clsAgent .
      ?clsAgent rdfs:subClassOf* techLayer1:UserAgent .
    }}
  }}
  {{
    SELECT (COUNT(DISTINCT ?clsEnt) AS ?countClsEnt)
    WHERE {{
      ?ent a ?clsEnt .
      ?clsEnt rdfs:subClassOf* techLayer1:Entity .
    }}
  }}
}}
"""

result = rdf_graph.query(query_class_counts)

for row in result:
    count_cls_rg = int(row.countClsRg)
    count_cls_agent = int(row.countClsAgent)
    count_cls_ent = int(row.countClsEnt)


# Totali istanze
total_instances = count_rg + count_agent + count_ent

# Totali classi distinte
total_classes = count_cls_rg + count_cls_agent + count_cls_ent

# Calcolo media complessiva istanze per classe
total_avg = round(total_instances / total_classes, 2) if total_classes > 0 else 0



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Cost': {
        'group': 'Sustainability',
        'conditions': {
            'Condition 1': total_avg
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================



#
# Condition 1:
# A Self-Sovereign Identity allows users to digitally encode their attributes.
#
#

existence = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
    ?pr a ?classProof .
    ?classProof rdfs:subClassOf* techLayer1:Proof .
    ?pr techLayer1:containsAttribute ?attr .
    ?attr a techLayer1:Attribute .
}}
"""

condition1 = rdf_graph.query(existence).askAnswer



#
# Conditon 2:
# Users can establish their existence in the digital realm.
#
#

existence = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
    ?h a techLayer1:Holder .
    ?h techLayer1:usesTrustTaskProtocol ?ttp .
    ?ttp a techLayer1:ProofPresentationProtocol .
    ?ttp techLayer1:presentationProof ?pr .
    ?pr a ?classProof .
    ?classProof rdfs:subClassOf* techLayer1:Proof .
}}
"""

condition2 = rdf_graph.query(existence).askAnswer



#
# Condition 3:
# By selectively sharing different sets of attributes, users can demonstrate their presence and even construct distinct identities based on various attribute combinations. This ability to manage multiple identities, each defined by a unique set of attributes, is fundamental to self-existence in the digital space.
#
#

existence = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?proof a ?classProof .
  ?classProof rdfs:subClassOf* techLayer1:Proof .

  ?proof techLayer1:containsAttribute ?attr1 .
  ?proof techLayer1:containsAttribute ?attr2 .

  FILTER (?attr1 != ?attr2)

  ?attr1 a techLayer1:Attribute .
  ?attr2 a techLayer1:Attribute .

  ?cred1 a ?credClass1 .
  ?credClass1 rdfs:subClassOf* techLayer1:Credential .
  ?cred1 techLayer1:encodesAttribute ?attr1 .

  ?cred2 a ?credClass2 .
  ?credClass2 rdfs:subClassOf* techLayer1:Credential .
  ?cred2 techLayer1:encodesAttribute ?attr2 .

  FILTER (?cred1 != ?cred2)
}}
"""

condition3 = rdf_graph.query(existence).askAnswer



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Existence': {
        'group': 'Controllability',
        'conditions': {
            "Condition 1": condition1,
            "Condition 2": condition2,
            "Condition 3": condition3
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1:
# A self-sovereign identity should be designed for maximum interoperability,
#
#

# Query per contare le istanze
check_query = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(DISTINCT ?aa) AS ?count)
WHERE {{
    ?aa a ?class .
    ?class rdfs:subClassOf* techLayer1:AdministeringAuthority .
}}
"""

# Esecuzione della query di conteggio
results = rdf_graph.query(check_query)
count = int([row["count"].value for row in results][0])

# Esegui controllo antecedente
antecedent_exists = count >= 2

if antecedent_exists:
    # Query 2: query principale
    main_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK WHERE {{
      ?aa a ?class .
      ?class rdfs:subClassOf* techLayer1:AdministeringAuthority .

      ?aa techLayer1:interactsWithAdministeringAuthority ?aa2 .
      ?aa2 a ?class2 .
      ?class2 rdfs:subClassOf* techLayer1:AdministeringAuthority .

      FILTER(?aa != ?aa2)
    }}
    """
    condition1 = rdf_graph.query(main_query).askAnswer
else:
    condition1 = None



#
# Condition 2:
# A self-sovereign identity should be designed for maximum interoperability,
#
#

# Query 1: controllo antecedente
check_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?rg a ?class .
  ?class rdfs:subClassOf* techLayer1:Registry .
}}
"""

# Esegui controllo antecedente
antecedent_exists = rdf_graph.query(check_query).askAnswer

if antecedent_exists:
    # Query 2: query principale
    main_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK WHERE {{
      ?rg a ?class .
      ?class rdfs:subClassOf* techLayer1:Registry .

      ?rg techLayer1:resolvesRegistry ?rg2 .

      ?rg2 a ?class2 .
      ?class2 rdfs:subClassOf* techLayer1:Registry .

      FILTER(?rg != ?rg2)
    }}
    """
    condition2 = rdf_graph.query(main_query).askAnswer
else:
    condition2 = None



#
# Condition 3:
# Ensuring broad accessibility and backward compatibility with legacy identity systems during a transitional period.
#
#


# Query per contare le istanze totali (GoverningAuthority e AdministeringAuthority)
query_total = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(DISTINCT ?instance) AS ?countTotal)
WHERE {{
  {{
    ?instance a ?class .
    ?class rdfs:subClassOf* techLayer1:GoverningAuthority .
  }}
  UNION
  {{
    ?instance a ?class2 .
    ?class2 rdfs:subClassOf* techLayer1:AdministeringAuthority .
  }}
}}
"""

# Query per contare le istanze TRUE, cioè che soddisfano la condizione
query_true = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(DISTINCT ?instance) AS ?countTrue)
WHERE {{
  {{
    ?ga a ?class .
    ?class rdfs:subClassOf* techLayer1:GoverningAuthority .
    
    ?ga techLayer1:governsRegistry ?rg .
    ?rg a ?class .
    ?class rdfs:subClassOf* techLayer1:Registry .
  
    ?rg techLayer1:resolvesRegistry ?rg2 .
    ?rg2 a ?class2 .
    ?class2 rdfs:subClassOf* techLayer1:Registry .
    
    FILTER(?rg != ?rg2)

    ?ga2 a ?class3 .
    ?class3 rdfs:subClassOf* techLayer1:GoverningAuthority .

    ?ga2 techLayer1:governsRegistry ?rg2 .

    FILTER(?ga != ?ga2)

    BIND(?ga AS ?instance)
  }}
  UNION
  {{
    ?aa a ?class .
    ?class rdfs:subClassOf* techLayer1:AdministeringAuthority .

    ?aa techLayer1:administersDigitalTrustUtility ?rg .
    ?rg a ?class4 .
    ?class4 rdfs:subClassOf* techLayer1:DigitalTrustUtility .

    ?rg techLayer1:resolvesRegistry ?rg2 .
    ?rg2 a ?class5 .
    ?class5 rdfs:subClassOf* techLayer1:DigitalTrustUtility .

    FILTER(?rg != ?rg2)

    ?aa2 techLayer1:administersDigitalTrustUtility ?rg2 .

    FILTER(?aa != ?aa2)

    BIND(?aa AS ?instance)
  }}
}}
"""

def get_count(query):
    qres = rdf_graph.query(query)
    for row in qres:
        return int(row[0])
    return 0

count_total = get_count(query_total)
count_true = get_count(query_true)

if count_total > 0:
    ratio_true = count_true / count_total
else:
    ratio_true = 0.0

condition3 = round(ratio_true, 2)



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Interoperability': {
        'group': 'Portability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================



#
# Condition 1:
# Identity systems should be flexible enough to allow users to share only the essential identity data necessary to achieve their goal.
#
#

info_zkp = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?zkp a ?zkpType .
  ?zkpType rdfs:subClassOf* techLayer1:ZeroKnowledgeProof .
}}
"""

condition1 = rdf_graph.query(info_zkp).askAnswer



#
# Condition 2:
# The disclosure of claims must be minimized as much as possible.
#
#

check_registrant_issuer = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?ra a techLayer1:Registrant .
  ?ra techLayer1:registersIssuer ?is .
  ?is a techLayer1:Issuer .
}}
"""

intermediate_result1 = rdf_graph.query(check_registrant_issuer).askAnswer


if intermediate_result1:
    # Se almeno uno esiste, esegui la query completa per contare le autorità decentralizzate vs totali
    info_registrant = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    SELECT (COUNT(DISTINCT ?ra) AS ?totalAdminAuthorities)
          (COUNT(DISTINCT ?ra_decentralized) AS ?decentralizedAdminAuthorities)
    WHERE {{
        ?ra a techLayer1:Registrant .
        ?ga a ?gaType .
        ?gaType rdfs:subClassOf* techLayer1:GoverningAuthority .
        ?ga techLayer1:delegatesAdministeringAuthority ?ra .

        OPTIONAL {{
            ?ga techLayer1:decentralized "true"^^xsd:boolean .
            BIND(?ra AS ?ra_decentralized)
        }}
    }}
    """
    results = rdf_graph.query(info_registrant)

    condition2 = 0.0  # valore di default
    for row in results:
        total = int(row["totalAdminAuthorities"])
        decentralized = int(row["decentralizedAdminAuthorities"])
        if total > 0:
            ratio = decentralized / total
            condition2 = round(ratio, 2)
        else:
            condition2 = 0.0
else:
    # Se nessuno dei due esiste, "salta" la query
    condition2 = None



#
# Condition 3:
# Identity systems should be flexible enough to allow users to share only the essential identity data necessary to achieve their goal.
#
#

check_registrant_verifier = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?ra a techLayer1:Registrant .
  ?ra techLayer1:registersVerifier ?vr .
  ?vr a techLayer1:Verifier .
}}
"""

intermediate_result2 = rdf_graph.query(check_registrant_verifier).askAnswer


if intermediate_result2:
    info_verifier = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    SELECT (COUNT(DISTINCT ?ra) AS ?totalAdminAuthorities)
          (COUNT(DISTINCT ?ra_decentralized) AS ?decentralizedAdminAuthorities)
    WHERE {{
        ?ra a techLayer1:Registrant .
        ?ga a ?gaType .
        ?gaType rdfs:subClassOf* techLayer1:GoverningAuthority .
        ?ga techLayer1:delegatesAdministeringAuthority ?ra .

        OPTIONAL {{
            ?ga techLayer1:decentralized "true"^^xsd:boolean .
            BIND(?ra AS ?ra_decentralized)
        }}
    }}
    """
    results = rdf_graph.query(info_verifier)

    condition3 = 0.0
    for row in results:
        total = int(row["totalAdminAuthorities"])
        decentralized = int(row["decentralizedAdminAuthorities"])
        if total > 0:
            condition3 = round(decentralized / total, 2)
        else:
            condition3 = 0.0
else:
    condition3 = None



#
# Condition 4:
# Any feature that increases correlation must be strictly controlled with the highest level of granularity.
#
#

check_exist_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  {{
    ?ra a ?raType .
    ?raType rdfs:subClassOf* techLayer1:AdministeringAuthority .
    ?ra techLayer1:registersIssuer ?is .
    ?is a techLayer1:Issuer .
  }}
  UNION
  {{
    ?ra a ?raType .
    ?raType rdfs:subClassOf* techLayer1:AdministeringAuthority .
    ?ra techLayer1:registersVerifier ?vr .
    ?vr a techLayer1:Verifier .
  }}
}}
"""

# Esegui il controllo preliminare
if rdf_graph.query(check_exist_query).askAnswer:
    # Se almeno uno esiste, esegui la query completa
    info_registrant = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK WHERE {{
      {{
        ?r1 a techLayer1:Registrant .
        ?r2 a techLayer1:Registrant .
        FILTER (?r1 != ?r2) .

        {{
          ?r1 techLayer1:registersIssuer|techLayer1:registersVerifier ?entity .
          ?r2 techLayer1:registersIssuer|techLayer1:registersVerifier ?entity .
        }}
      }}
      UNION
      {{
        ?r a techLayer1:Registrant .
        ?r techLayer1:registersIssuer ?is .
        ?is a techLayer1:Issuer .
        ?r techLayer1:registersVerifier ?vr .
        ?vr a techLayer1:Verifier .
      }}
    }}
    """

    condition4 = not(rdf_graph.query(info_registrant).askAnswer)
else:
    # Se nessuno dei due esiste, "salta" la query
    condition4 = None  # oppure None, o altro comportamento desiderato



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Minimal disclosure': {
        'group': 'Security',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3,
            'Condition 4': condition4
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1
# Identity must persist for as long as users desire, remaining valid even if the identity provider no longer exists.
#
#

query_ask_multiple_issuers = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?is techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:CredentialIssuanceProtocol .
  ?ttp techLayer1:issuanceCredential ?cr1 .
  ?cr1 a ?class2 .
  ?class2 rdfs:subClassOf* techLayer1:Credential .
  ?cr1 techLayer1:encodesAttribute ?attr .
  ?attr a techLayer1:Attribute .

  ?is2 techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:CredentialIssuanceProtocol .
  ?ttp techLayer1:issuanceCredential ?cr2 .
  ?cr2 a ?class4 .
  ?class4 rdfs:subClassOf* techLayer1:Credential .
  ?cr2 techLayer1:encodesAttribute ?attr .

  FILTER(?is != ?is2)
}}
"""

condition1 = rdf_graph.query(query_ask_multiple_issuers).askAnswer



#
# Condition 2
# To ensure this, individuals should be able to self-assert attributes
#
#

# Query per verificare la presenza di attributi self-issued (booleano)
query_self_issued_attributes_in_proofs = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>
ASK {{
  ?pr a ?class .
  ?class rdfs:subClassOf* techLayer1:Proof .
  ?pr techLayer1:containsAttribute ?attr1 .
  ?attr1 a techLayer1:Attribute .

  FILTER NOT EXISTS {{
    ?ttp techLayer1:issuanceCredential ?cr .
    ?cr a ?class2 .
    ?class2 rdfs:subClassOf* techLayer1:Credential .
    ?cr techLayer1:encodesAttribute ?attr2 .
    ?attr2 a techLayer1:Attribute .

    FILTER(?attr1 = ?attr2)
  }}
}}
"""

condition2 = rdf_graph.query(query_self_issued_attributes_in_proofs).askAnswer



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Persistence': {
        'group': 'Security',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1:
# Digital identity data must be transferable across platforms, ensuring continuity even if the original platform ceases to exist.
#
#

query_ask_multi_trust_member = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?id techLayer1:identifiesEntity ?act .
  ?id a ?classId .
  ?classId rdfs:subClassOf* techLayer1:Identifier .

  ?act a ?classAct .
  ?classAct rdfs:subClassOf* techLayer1:Actor .
  ?act techLayer1:memberOfTrustCommunity ?tc1, ?tc2 .
  ?tc1 a techLayer1:TrustCommunity .
  ?tc2 a techLayer1:TrustCommunity .

  ?gf1 a techLayer1:GovernanceFramework .
  ?gf2 a techLayer1:GovernanceFramework .
  ?gf1 techLayer1:rulesParty ?tc1 .
  ?gf2 techLayer1:rulesParty ?tc2 .

  ?id2 techLayer1:identifiesEntity ?act .
  ?id2 a ?classId2 .
  ?classId2 rdfs:subClassOf* techLayer1:Identifier .

  FILTER(?id = ?id2)
  FILTER(?gf1 != ?gf2)
  FILTER(?tc1 != ?tc2)
}}
"""

condition1 = rdf_graph.query(query_ask_multi_trust_member).askAnswer



#
# Condition 2
# This includes the ability to [move or ]copy one’s digital identity data to chosen agents or systems.
#
#

query_ask_backup_path = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?rg a ?class .
  ?class rdfs:subClassOf* techLayer1:Registry .

  {{
    ?tru techLayer1:ExternalBackup ?tp .
    ?tp a ?ClassTp .
    ?ClassTp rdfs:subClassOf* techLayer1:IntermediarySystem .
  }}  
  UNION
  {{
    ?dv techLayer1:LocalBackup ?dv2 .
    ?dv2 a techLayer1:DataVault .
  }}
}}
"""

condition2 = rdf_graph.query(query_ask_backup_path).askAnswer



#
# Condition 3
# The transfer should be seamless and free from legal, political, or technological barriers[, even in the face of disasters].
#
#

# GoverningAuthority query
query_governing = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?rg a ?classRg .
  ?rg2 a ?classRg2 .
  ?classRg rdfs:subClassOf* techLayer1:Registry .
  ?classRg2 rdfs:subClassOf* techLayer1:Registry .

  ?ga a techLayer1:GoverningAuthority .
  ?ga2 a techLayer1:GoverningAuthority .
  ?ga techLayer1:governsRegistry ?rg .
  ?ga2 techLayer1:governsRegistry ?rg2 .

  FILTER(?ga != ?ga2)
}}
"""

# AdministeringAuthority query
query_administering = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?aa a ?classAa .
  ?classAa rdfs:subClassOf* techLayer1:AdministeringAuthority .
  ?aa2 a ?classAa2 .
  ?classAa2 rdfs:subClassOf* techLayer1:AdministeringAuthority .

  ?aa techLayer1:administersDigitalTrustUtility ?tr .
  ?aa2 techLayer1:administersDigitalTrustUtility ?tr2 .

  ?tr a ?class1 .
  ?tr2 a ?class2 .
  ?class1 rdfs:subClassOf* techLayer1:Registry .
  ?class2 rdfs:subClassOf* techLayer1:Registry .

  FILTER(?aa != ?aa2)
}}
"""

# Esegui le query ASK
governing_result = rdf_graph.query(query_governing).askAnswer
administering_result = rdf_graph.query(query_administering).askAnswer

# Calcola il punteggio finale
condition3 = 0.0
if governing_result:
    condition3 += 0.5
if administering_result:
    condition3 += 0.5



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Portability': {
        'group': 'Portability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1:
# All identity information should be securely stored.
#
#

# Prima: controlla se il DataVault mantiene credenziali valide
query_cred_check = f"""\
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?dv a techLayer1:DataVault ;
     techLayer1:maintainsCredential ?cr .
  ?cr a ?class .
  ?class rdfs:subClassOf* techLayer1:Credential .
}}
"""

# Seconda: verifica se esiste almeno un identificatore legato a un holder
query_identifier_exists = f"""\
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?holder techLayer1:hasIdentifier ?id .
  ?id a ?class2 .
  ?class2 rdfs:subClassOf* techLayer1:Identifier .
}}
"""

# Terza: verifica se tale identificatore è memorizzato dal DataVault
query_identifier_stored = f"""\
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?dv a techLayer1:DataVault .
  ?dv techLayer1:storesIdentifier ?id .
  ?id a ?class3 .
  ?class3 rdfs:subClassOf* techLayer1:Identifier .
}}
"""

# Esecuzione delle query con fallback in caso di errore
try:
    credential_ok = rdf_graph.query(query_cred_check).askAnswer
    identifier_exists = rdf_graph.query(query_identifier_exists).askAnswer
    identifier_stored = rdf_graph.query(query_identifier_stored).askAnswer
except Exception as e:
    print("Errore durante l'esecuzione delle query SPARQL:", e)
    credential_ok = False
    identifier_exists = False
    identifier_stored = False

# Logica per assegnare il punteggio finale
if not credential_ok:
    condition1 = 0.0
elif identifier_exists:
    if identifier_stored:
        condition1 = 1.0
    else:
        condition1 = 0.5
else:
    condition1 = 1.0 if credential_ok else 0.0  # già coperto dal primo if, ma esplicito


#
# Condition 2:
# [identity information] transmitted through protected channels.
#
#

info_securely_transmitted = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?ua a techLayer1:UserAgent .
  ?ua techLayer1:enablesTSP ?auth .
  ?auth a ?actualType .

  techLayer1:AuthenticationProtocol rdfs:subClassOf* ?actualType .
}}
"""

condition2 = rdf_graph.query(info_securely_transmitted).askAnswer



#
# Condition 3:
# Priority should be given to[ censorship-resistant systems that uphold] individual rights and freedoms within decentralized environments.
#
#

# Query per contare i registri totali e quelli decentralizzati
decentralized_environment = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(?rg) AS ?totalRegistries) (COUNT(?decentralizedRg) AS ?decentralizedRegistries)
WHERE {{
  ?rg a ?classRg .
  ?classRg rdfs:subClassOf* techLayer1:Registry .
  OPTIONAL {{
    ?rg techLayer1:hasArchitectureType ?da .
    ?da a techLayer1:DecentralizedArchitecture .
    BIND(?rg AS ?decentralizedRg)
  }}
}}
"""

results = rdf_graph.query(decentralized_environment)

for row in results:
    total = int(row.totalRegistries.toPython())
    decentralized = int(row.decentralizedRegistries.toPython())

condition3 = decentralized / total if total > 0 else 0
condition3 = round(condition3, 2)



#
# Condition 4:
# Priority should be given to[ censorship-resistant systems that uphold] individual rights and freedoms within decentralized environments.
#
#

censorship_resistant = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?tsp a techLayer1:TrustedCommunicationProtocol .
  ?tsp techLayer1:routesThroughIntermediarySystem ?int .
  ?int a ?classInt .
  ?classInt rdfs:subClassOf* techLayer1:IntermediarySystem .
}}
"""

condition4 = not(rdf_graph.query(censorship_resistant).askAnswer)



#
# Condition 5:
# Priority should be given to censorship-resistant systems[ that uphold individual rights and freedoms within decentralized environments].
#
#

censorship_resistant = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (xsd:float(?decentralizedCount) / xsd:float(?totalCount) AS ?percentage)
WHERE {{
  {{
    SELECT (COUNT(DISTINCT ?ga) AS ?totalCount)
    WHERE {{
      ?ga a ?classGa .
      ?classGa rdfs:subClassOf* techLayer1:GoverningAuthority .
    }}
  }}
  {{
    SELECT (COUNT(DISTINCT ?ga) AS ?decentralizedCount)
    WHERE {{
      ?ga a ?classGa .
      ?classGa rdfs:subClassOf* techLayer1:GoverningAuthority .
      ?ga techLayer1:decentralized true .
    }}
  }}
}}
"""

result = rdf_graph.query(censorship_resistant)

condition5 = None
for row in result:
    condition5 = float(row.percentage)  # usa 'percentage' come nome variabile
    break  # prendi il primo risultato

condition5 = round(condition5, 2)



#
# Condition 6:
# Identities must be safeguarded using state-of-the-art security mechanisms and technologies.
#
#

state_of_the_art = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT ( (COUNT(DISTINCT ?type) * 1.0 / 8) AS ?percentage )
WHERE {{
  {{
    ?vc a techLayer1:VC .
    BIND("vc" AS ?type)
  }} UNION {{
    ?kms a techLayer1:KeyManagementSystem .
    BIND("kms" AS ?type)
  }} UNION {{
    ?ep a techLayer1:EncryptionProtocol .
    BIND("ep" AS ?type)
  }} UNION {{
    ?auth a techLayer1:AuthenticationProtocol .
    BIND("auth" AS ?type)
  }} UNION {{
    ?pr a ?classPr .
    ?classPr rdfs:subClassOf* techLayer1:Proof .
    BIND("pr" AS ?type)
  }} UNION {{
    ?aud a techLayer1:Auditor .
    BIND("aud" AS ?type)
  }} UNION {{
    ?vdr a techLayer1:VDR .
    BIND("vdr" AS ?type)
  }} UNION {{
    ?dv a techLayer1:DataVault .
    BIND("dv" AS ?type)
  }}
}}
"""

# Esecuzione della query e lettura del risultato
result = rdf_graph.query(state_of_the_art)

condition6 = 0.0  # default in caso di risultato vuoto
for row in result:
    condition6 = float(row.percentage)  # valore tra 0 e 1

condition6 = round(condition6, 2)



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Security': {
        'group': 'Security',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3,
            'Condition 4': condition4,
            'Condition 5': condition5,
            'Condition 6': condition6
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================



#
# Condition 1:
# Identity systems should be built on open standards. [Entities must be represented, exchanged, secured, protected, and verified using open, public, and royalty-free standards.]
#
#

technical_standard_count = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(?ts) AS ?total) (SUM(IF(BOUND(?open) && ?open = true, 1, 0)) AS ?openCount)
WHERE {{
  ?ts a ?class .
  ?class rdfs:subClassOf* techLayer1:TechnicalStandard .

  OPTIONAL {{ ?ts techLayer1:open ?open . }}
}}
"""

result = rdf_graph.query(technical_standard_count)

total = 0
open_count = 0
for row in result:
    total = int(row.total)
    open_count = int(row.openCount)

if total > 0:
    condition1 = (open_count / total)
else:
    condition1 = 0.0

condition1 = round(condition1, 2)



#
# Condition 2:
# Identity systems should be built on open standards.
#
#

technology_provider_adoption_rate = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(DISTINCT ?tp) AS ?totalTP)
       (COUNT(DISTINCT ?tpAdopter) AS ?adoptingTP)
       ((COUNT(DISTINCT ?tpAdopter) / COUNT(DISTINCT ?tp)) AS ?adoptionRate)
WHERE {{
    ?tp a ?classTp .
    ?classTp rdfs:subClassOf* techLayer1:TechnologyProvider .

    OPTIONAL {{
        ?tpAdopter a ?class2 .
        ?class2 rdfs:subClassOf* techLayer1:TechnologyProvider .
        ?tpAdopter techLayer1:adoptsTechnicalStandard ?standard .
        ?standard techLayer1:open ?open . 
  }}
}}
"""

# Esegui la query per condition 2
result = rdf_graph.query(technology_provider_adoption_rate)

total_tp = 0
adopting_tp = 0
condition2 = 0.0

for row in result:
    total_tp = int(row.totalTP)
    adopting_tp = int(row.adoptingTP)
    if total_tp > 0:
        condition2 = adopting_tp / total_tp

# Arrotonda a 1 cifra decimale
condition2 = round(condition2, 2)



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Standard': {
        'group': 'Sustainability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1
# The identity system, [along with the algorithms and protocols used for identity management,] should be open to ensure transparency in rules, policies, and procedures.
#
#

# Query per contare istanze di GovernanceFramework
count_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT (COUNT(?gf) AS ?total)
WHERE {{
  ?gf a ?class .
  ?class rdfs:subClassOf* techLayer1:GovernanceFramework .
}}
"""

count_result: SPARQLResult = rdf_graph.query(count_query)
total = int(list(count_result)[0].total)

# Se ci sono istanze, calcola la percentuale di quelle con open=true
if total > 0:
    open_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>
    PREFIX xsd: <{XSD}>

    SELECT (SUM(?openVal) AS ?openCount)
    WHERE {{
      ?gf a techLayer1:GovernanceFramework .
      OPTIONAL {{
        ?gf techLayer1:open ?open .
        BIND(IF(?open = "true"^^xsd:boolean, 1, 0) AS ?openVal)
      }}
      BIND(COALESCE(?openVal, 0) AS ?openVal)
    }}
    """
    open_result: SPARQLResult = rdf_graph.query(open_query)
    open_count = int(list(open_result)[0].openCount)

    condition1 = round(open_count / total, 2)
else:
    condition1 = None



#
# Condition 2
# Users must have clear visibility into their identities and related interactions.
#
#

# === VERIFICA PRESENZA DI storesCredential ===
stores_credential_pred = URIRef(f"{TECH_LAYER1_NS}storesCredential")
has_stores_credential = any(
    rdf_graph.triples((None, stores_credential_pred, None))
)

# === CONDIZIONE: Verifica coerenza tra storesCredential e AuthoritativeSource ===
if has_stores_credential:
    query_check_authoritative_source_match_credential = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK {{
      ?as1 a techLayer1:AuthoritativeSource .
      ?as1 techLayer1:storesCredential ?cr .
      ?cr a ?class .
      ?class rdfs:subClassOf* techLayer1:Credential .

      ?h a techLayer1:Holder .
      ?h techLayer1:holderConsultsAuthoritativeSource ?as2 .

      FILTER(?as1 = ?as2)
    }}
    """

    is_match_credential = bool(rdf_graph.query(query_check_authoritative_source_match_credential).askAnswer)
else:
    is_match_credential = None

# === VERIFICA PRESENZA DI storesProof ===
stores_proof_pred = URIRef(f"{TECH_LAYER1_NS}storesProof")
has_stores_proof = any(
    rdf_graph.triples((None, stores_proof_pred, None))
)

if has_stores_proof:
    query_check_authoritative_source_match_proof = f"""
    PREFIX techLayer1: <{TECH_LAYER1_NS}>

    ASK {{
      ?as a techLayer1:AuthoritativeSource .
      ?as techLayer1:storesProof ?pr .
      ?pr a ?class .
      ?class rdfs:subClassOf* techLayer1:Proof .

      ?h a techLayer1:Holder .
      ?h techLayer1:holderConsultsAuthoritativeSource ?as .
    }}
    """

    is_match_proof = bool(rdf_graph.query(query_check_authoritative_source_match_proof).askAnswer)
else:
    is_match_proof = None

# Funzione per combinare le condizioni
def combine_conditions(cond1, cond2):
    conditions = [cond1, cond2]

    # Filtra solo i valori che non sono None
    valid_conditions = [c for c in conditions if c is not None]

    if not valid_conditions:
        return None  # Nessuna condizione disponibile

    true_count = sum(1 for c in valid_conditions if c is True)
    total_conditions = len(valid_conditions)

    return round(true_count / total_conditions, 1)

# Combinazione sicura delle condizioni
condition2 = combine_conditions(is_match_credential, is_match_proof)



#
# Condition 3
# Users must have clear visibility into their identities and related interactions.
#
#

query_check_data_wallet = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
    ?h a techLayer1:Holder .
    ?h techLayer1:agencyOfUserAgent ?ua .
    ?ua a techLayer1:UserAgent .
    ?ua techLayer1:hasDataVault ?dv .
    ?dv a techLayer1:DataVault .
    ?dv techLayer1:maintainsCredential ?cr .
    ?cr a ?class .
    ?class rdfs:subClassOf* techLayer1:Credential .
}}
"""

condition3 = bool(rdf_graph.query(query_check_data_wallet).askAnswer)



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Transparency': {
        'group': 'Portability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1:
# An SSI ecosystem must prioritize user experience by ensuring that agents are highly usable and offer a consistent, intuitive interface.
#
#

usability = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?h a techLayer1:Holder .
  ?h techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:OutOfBandProtocol .

  ?v a techLayer1:Verifier .
  ?v techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:OutOfBandProtocol .
}}
"""

issuer_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?h a techLayer1:Holder .
  ?h techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:OutOfBandProtocol .

  ?iss a techLayer1:Issuer .
  ?iss techLayer1:usesTrustTaskProtocol ?ttp .
  ?ttp a techLayer1:OutOfBandProtocol .
}}
"""

holder_verifier = rdf_graph.query(usability).askAnswer
issuer_uses = rdf_graph.query(issuer_query).askAnswer

if holder_verifier and issuer_uses:
    condition1 = 1.0
elif holder_verifier:
    condition1 = 0.5
else:
    condition1 = 0.0



#
# Condition 2:
# This allows entities to reliably and effectively [control, ]manage, and utilize their identities.
#
#

usability = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  ?h a techLayer1:Holder .
  ?h techLayer1:agencyOfUserAgent ?ua .
  ?ua a techLayer1:UserAgent .
  ?ua techLayer1:hasKeyManagementSystem ?kms .
  ?kms a techLayer1:KeyManagementSystem .
  ?kms techLayer1:managesIdentifier ?id .
  ?id a ?class2 .
  ?class2 rdfs:subClassOf* techLayer1:Identifier .
}}
"""

condition2 = rdf_graph.query(usability).askAnswer



#
# Condition 3:
# Additionally, the system should simplify underlying complexities, making it easy to use.
#
#

# Query per edgeAgent
edge_agent_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
    ?h a techLayer1:Holder .
    ?h techLayer1:agencyOfUserAgent ?ua .
    ?ua a techLayer1:UserAgent .
    ?ua techLayer1:edgeAgent true .
}}
"""

# Query per cloudAgent
cloud_agent_query = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
    ?h a techLayer1:Holder .
    ?h techLayer1:agencyOfUserAgent ?ua .
    ?ua a techLayer1:UserAgent .
    ?ua techLayer1:cloudAgent true .
}}
"""

# Esegui le query
has_edge_agent = rdf_graph.query(edge_agent_query).askAnswer
has_cloud_agent = rdf_graph.query(cloud_agent_query).askAnswer

# Assegna il valore a condition3
if has_edge_agent and has_cloud_agent:
    condition3 = 1.0
elif has_edge_agent or has_cloud_agent:
    condition3 = 0.5
else:
    condition3 = 0.0



# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Usability': {
        'group': 'Usability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


#
# Condition 1:
# An SSI ecosystem must empower identity holders to provide verifiable proof of the authenticity of their digital identity data.
#
#

# Definizione della query SPARQL per contare istanze specifiche e totali per ciascuna categoria
count_query = f"""
PREFIX techLayer1: <{TECH_LAYER1_NS}>

SELECT 
  (COUNT(DISTINCT ?vid) AS ?numVIDs)
  (COUNT(DISTINCT ?allId) AS ?totalIdentifiers)
  (COUNT(DISTINCT ?vc) AS ?numVCs)
  (COUNT(DISTINCT ?allCred) AS ?totalCredentials)
  (COUNT(DISTINCT ?vdr) AS ?numVDRs)
  (COUNT(DISTINCT ?allReg) AS ?totalRegistries)
WHERE {{
  OPTIONAL {{
    ?vid a ?classVid .
    ?classVid rdfs:subClassOf* techLayer1:VID .
  }}
  OPTIONAL {{
    ?allId a ?classId .
    ?classId rdfs:subClassOf* techLayer1:Identifier .
  }}
  OPTIONAL {{
    ?vc a ?classVC .
    ?classVC rdfs:subClassOf* techLayer1:VC .
  }}
  OPTIONAL {{
    ?allCred a ?classCred .
    ?classCred rdfs:subClassOf* techLayer1:Credential .
  }}
  OPTIONAL {{
    ?vdr a ?classVDR .
    ?classVDR rdfs:subClassOf* techLayer1:VDR .
  }}
  OPTIONAL {{
    ?allReg a ?classReg .
    ?classReg rdfs:subClassOf* techLayer1:Registry .
  }}
}}
"""

# Esecuzione della query SPARQL sul grafo RDF
results = rdf_graph.query(count_query)

# Estrazione e calcolo dei risultati
for row in results:
    num_vids = int(row.numVIDs)
    total_identifiers = int(row.totalIdentifiers)

    num_vcs = int(row.numVCs)
    total_credentials = int(row.totalCredentials)

    num_vdrs = int(row.numVDRs)
    total_registries = int(row.totalRegistries)

    # Somma delle istanze specifiche
    numeratore = num_vids + num_vcs + num_vdrs
    # Somma delle istanze totali delle rispettive classi madri e sottoclassi
    denominatore = total_identifiers + total_credentials + total_registries

    # Calcolo del rapporto come valore tra 0 e 1
    condition1 = round(numeratore / denominatore, 2) if denominatore > 0 else 0.0

    print("condition1 =", condition1)



#
# Condition 2:
# At the same time, relying parties should be able to verify this data without direct interaction with the issuers.
#
#

verifiability = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{

    ?iss a techLayer1:Issuer .
    ?iss techLayer1:usesTrustTaskProtocol ?iex .
    ?iex a ?actualType .
    techLayer1:IdentifierExchangeProtocol rdfs:subClassOf* ?actualType .

    ?h a techLayer1:Holder .
    ?h techLayer1:usesTrustTaskProtocol ?iex .
    ?iex a ?actualType2 .
    techLayer1:IdentifierExchangeProtocol rdfs:subClassOf* ?actualType2 .

    ?vr a techLayer1:Verifier .
    ?vr techLayer1:usesTrustTaskProtocol ?iex .
    ?iex a ?actualType3 .
    techLayer1:IdentifierExchangeProtocol rdfs:subClassOf* ?actualType3 .

}}
"""

condition2 = rdf_graph.query(verifiability).askAnswer



#
# Condition 3:
# At the same time, relying parties should be able to verify this data without direct interaction with the issuers.
#
#

issuer_registered = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
  FILTER EXISTS {{
    ?iss a techLayer1:Issuer .
    ?iss techLayer1:issuerRegisteredInRegistry ?rg .
    ?rg a ?class .
    ?class rdfs:subClassOf* techLayer1:Registry .
  }}
}}
"""

result = rdf_graph.query(issuer_registered).askAnswer

if result:
    verifiability = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK WHERE {{
    ?iss a techLayer1:Issuer .
    ?iss techLayer1:issuerRegisteredInRegistry ?rg .
    ?rg a ?class .
    ?class rdfs:subClassOf* techLayer1:Registry .

    ?vr a techLayer1:Verifier .
    ?vr techLayer1:usesTrustTaskProtocol ?ttp .
    ?ttp a ?ttpType .
    ?ttpType rdfs:subClassOf* techLayer1:TrustTaskProtocol .

    ?ttp techLayer1:consultsRegistry ?rg .

    FILTER (?ttpType = techLayer1:TrustRegistryProtocol) 
}}"""
    condition3 = rdf_graph.query(verifiability).askAnswer
else:
    condition3 = None



#
# Condition 4:
# They must receive objective evidence that the presented digital identities accurately represent their rightful owners.
#
#

authentication_protocol = f"""PREFIX techLayer1: <{TECH_LAYER1_NS}>

ASK {{
  ?ua a techLayer1:UserAgent .
  ?ua techLayer1:enablesTSP ?auth .
  ?auth a ?actualType .

  techLayer1:AuthenticationProtocol rdfs:subClassOf* ?actualType .
}}
"""

condition4 = rdf_graph.query(authentication_protocol).askAnswer




# === STAMPA DELLA STRUTTURA ===
# === CREAZIONE STRUTTURA DATI FINALE ===
access_conditions = {
    'Verifiability': {
        'group': 'Usability',
        'conditions': {
            'Condition 1': condition1,
            'Condition 2': condition2,
            'Condition 3': condition3
            #'Condition 4': condition4
        }
    }
}

result_condition.update(access_conditions)

# =====================================
# =====================================
# =====================================
# =====================================
# =====================================
# =====================================


print(result_condition)



# =====================================
# PRINT GRAPH
# =====================================

import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# ======================
# SUPPORT FUNCTION
# ======================

def compute_percentage(principle_name, principle_data):
    # Special case for 'Standard'
    if principle_name == 'Standard':
        conditions = principle_data['conditions']
        value = conditions.get('Condition 1', 0)
        if value is None:
            value = 0
        percentage = value * 100
        return percentage, 1

    # Special case for 'Cost'
    if principle_name == 'Cost':
        conditions = principle_data['conditions']
        value = next((v for v in conditions.values() if isinstance(v, (int, float))), None)
        if value is None or value <= 0:
            return 0, 1
        min_value = 1
        score = 100 * (min_value / value)
        return max(0, min(100, score)), 1

    # General case
    conditions = principle_data['conditions']

    # Filter out None values
    filtered_values = {k: v for k, v in conditions.items() if v is not None}

    # Convert booleans to 0/1
    bool_values = [(1 if v is True else 0) for v in filtered_values.values() if isinstance(v, bool)]
    bool_weights = [1] * len(bool_values)

    # Numeric values (excluding bools)
    numeric_values = [v for v in filtered_values.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    numeric_weights = [1] * len(numeric_values)

    # Combine all
    all_values = bool_values + numeric_values
    all_weights = bool_weights + numeric_weights

    if not all_values:
        return 0, 1

    weighted_sum = sum(val * w for val, w in zip(all_values, all_weights))
    total_weight = sum(all_weights)
    weighted_average = weighted_sum / total_weight

    percentage = weighted_average * 100
    return percentage, total_weight

# ======================
# COLOR CONFIGURATION
# ======================

group_colors_map = {
    'Usability': '#00FF00',       # verde neon
    'Controllability': '#FFA500', # arancione puro
    'Sustainability': '#9400D3',  # viola acceso
    'Security': '#FF0000',        # rosso puro
    'Portability': '#1E90FF'      # blu acceso
}

# ======================
# DATA PROCESSING
# ======================

sorted_items = sorted(result_condition.items(), key=lambda x: x[1]['group'])

labels = []
percentages = []
group_labels = []

# For weighted mean
group_weighted_values = defaultdict(list)

for principle, data in sorted_items:
    perc, weight = compute_percentage(principle, data)
    labels.append(principle)
    percentages.append(perc)
    group_labels.append(data['group'])
    group_weighted_values[data['group']].append((perc, weight))

# Compute weighted mean per group
group_means_map = {
    group: sum(perc * weight for perc, weight in values) / sum(weight for _, weight in values)
    for group, values in group_weighted_values.items()
}
mean_per_principle = [group_means_map[g] for g in group_labels]

# ======================
# RADAR CHART SETUP
# ======================

num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Close the chart
angles += angles[:1]
percentages += percentages[:1]
mean_per_principle += mean_per_principle[:1]
labels += labels[:1]
group_labels += group_labels[:1]

fig, ax = plt.subplots(figsize=(12, 12), subplot_kw=dict(polar=True))

background_alpha = 0.45
for i in range(num_vars):
    color = group_colors_map.get(group_labels[i], 'gray')
    ax.bar(
        x=angles[i],
        height=100,
        width=2 * np.pi / num_vars,
        bottom=0,
        color=color,
        alpha=background_alpha,
        edgecolor='none',
        zorder=0
    )

# ax.plot(angles, percentages, color='blue', linewidth=2, label='Individual Principles', zorder=3)
# ax.fill(angles, percentages, color='blue', alpha=0.25, zorder=2)

ax.plot(angles, mean_per_principle, color='red', linewidth=2, linestyle='dashed', label='Average per Group', zorder=4)
ax.fill(angles, mean_per_principle, color='red', alpha=0.15, zorder=1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels[:-1], fontsize=10)

yticks = [25, 50, 75]
ax.set_yticks(yticks)
ax.set_yticklabels([f'{y}%' for y in yticks])
ax.set_ylim(0, 100)

# ======================
# LEGEND
# ======================

legend_patches = [
    Patch(color=color, label=f"Group: {group}")
    for group, color in group_colors_map.items()
]

legend_lines = [
    # Line2D([0], [0], color='blue', linewidth=2, label='Value per principle'),
    Line2D([0], [0], color='red', linewidth=5, linestyle='dashed', label='Weighted Average per Group')
]

first_legend = ax.legend(handles=legend_patches, loc='upper right', bbox_to_anchor=(1.3, 1.05), title="Group Colors")
second_legend = ax.legend(handles=legend_lines, loc='upper right', bbox_to_anchor=(1.3, 0.85), title="Value Lines")

ax.add_artist(first_legend)

plt.tight_layout()
plt.show()
