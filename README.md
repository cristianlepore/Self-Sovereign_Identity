# Self-Sovereign Identity — Semantic Framework and Evaluation Resources

**Author:** Cristian Lepore  
**Affiliation:** Université de Toulouse, IRIT Laboratory  
**Thesis:** *A Semantic Framework for Defining and Assessing e-Identity Management Ecosystems Based on Self-Sovereign Identity Principles* (Ph.D. Candidate, 2025)  

---

## Overview

This repository contains the **ontologies, principles, scripts, and datasets** developed within the doctoral research on **Self-Sovereign Identity (SSI)**.  
These resources implement and validate a **semantic framework** for modeling and evaluating **digital identity ecosystems** in accordance with SSI principles and the Trust over IP (ToIP) reference architecture.

All materials are organized to promote **transparency**, **reproducibility**, and **reusability** for both academic and applied research contexts.

---

## Repository Structure

### Theoretical Foundations

#### 1. Kernel Theories (KT)
**File:** [`Kernel_Theories/kernel_theories.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/kernel_theories/kernel_theories.md)

This section presents the **foundational theories** underpinning the semantic and evaluative framework.  
Each Kernel Theory corresponds to one or more **Design Principles (DPs)** drawn from the ToIP and SSI paradigms.

Schema employed:
> **Design Principle → Objective (Why) → Mechanism (How) → Conditions (Where/When) → Kernel Theories → Method of Derivation**

Representative examples include:
- **End-to-End Principle** — Saltzer, Reed & Clark (1984)  
- **Modularity & Layering** — Baldwin & Clark (2000)  
- **Public Key Cryptography Theory** — Diffie & Hellman (1976); Rivest et al. (1978)  
- **Privacy by Design** — Cavoukian (2009)  
- **Relational Theory of Trust** — Hardin (2002)  
- **Value Sensitive Design / Responsible Innovation** — Friedman et al. (2002); Stilgoe et al. (2013)

These Kernel Theories constitute the **epistemic foundation** of the ontology, grounding the model in rigorous interdisciplinary theory.

---

### SSI Principles and Conceptual Model

#### 2. Principles of Self-Sovereign Identity
**File:** [`principles_of_ssi.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/principles_of_ssi.md)

A harmonized set of **SSI principles** derived from a systematic literature review and expert validation.  
Each principle includes:
- A definition  
- Source references  
- Assigned category  

#### 3. Principles and Categories Table
**Link:** [Principles_and_categories.html](https://cristianlepore.github.io/Self-Sovereign_Identity/Principles_and_categories.html)

Interactive HTML visualization illustrating the **clustering of SSI principles** into thematic domains (corresponding to Table 5.3 in the thesis).

#### 4. Final List of SSI Principles
**Path:** [`/definition_of_principles.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/definition_of_principles.md)

Consolidated and validated list of principles used in the evaluation of **case studies** (eIDAS, Sovrin, Bhutan NDI).

---

### Ontologies

#### 5. Reference Ontology (ToIP)
**Path:** [`/ontologie/toip`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main/ontologies/toip)

This directory contains the **reference ontology**, developed in RDF/OWL, which operationalizes the **semantic framework** proposed in the thesis.  
It models the **four-layer Trust over IP (ToIP) architecture** — *Technology*, *Utility*, *Governance*, and *Ecosystem* — through formal classes, properties, and relationships linking **technical entities** with **normative and ethical values**.

The ontology serves as the **conceptual core** of the framework, enabling semantic reasoning, interoperability, and the assessment of digital identity ecosystems in line with **Self-Sovereign Identity** principles.

#### 6. Ontologies for Case Studies
**Path:** [`/ontologies`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main/ontologies)

Includes ontology instances for selected real-world identity systems:
- eIDAS  
- Sovrin  
- PKIX  
- uPort  
- Bhutan NDI  

These instances are used to **validate and compare** systems within the semantic evaluation model.

---

### Analytical and Computational Tools

#### 7. Subject–Verb–Object (SVO) Extraction — Python Scripts
**Path:** [`/nlp/BERT.py`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/nlp/BERT.py)

Python scripts implementing the **Subject–Verb–Object (SVO)** model to extract fundamental relational structures.  
These outputs support the generation of ontology instances and the mapping of principles to entities.

#### 8. Clustering Techniques
**Path:** [`/clustering`](https://github.com/cristianlepore/Self-Sovereign_Identity/tree/main/clustering)

Includes scripts for:
- **K-Means Clustering**  
- **Louvain Algorithm**  
- **Greedy Optimization**

Used to identify conceptual clusters of SSI principles, as described in **Appendix B** of the thesis.

#### 9. SPARQL Queries
**File:** [`queries/sparql.py`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/queries/sparql.py)

Contains **SPARQL queries** employed within the *Principle Engine* to extract and score relationships between principles, indicators, and system components.

---

### Libraries and Dependencies

**File:** [`libraries.md`](https://github.com/cristianlepore/Self-Sovereign_Identity/blob/main/libraries.md)

This section provides a dependency overview for all Python scripts included in the repository.  
Most scripts rely on **NumPy** for numerical computation and **Matplotlib** for data visualization, while ontology-related scripts use **Owlready2** for semantic reasoning.

#### Core Libraries
- **NumPy (`np`)** — numerical operations, matrix manipulation, and statistical computation  
- **Matplotlib (`plt`, `ax`)** — plotting and visualization utilities  
- **Owlready2 (`get_ontology`, `sync_reasoner`, `URIRef`, `rdf_graph`)** — ontology management and RDF/OWL reasoning  

---

### Citation (BibTeX)

```bibtex
@phdthesis{lepore2025ssi,
  author    = {Cristian Lepore},
  title     = {A Semantic Framework for Defining and Assessing e-Identity Management Ecosystems Based on Self-Sovereign Identity Principles},
  school    = {Université de Toulouse},
  year      = {2025},
  address   = {Toulouse, France}
}
