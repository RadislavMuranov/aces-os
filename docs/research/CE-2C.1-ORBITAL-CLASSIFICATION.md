# ACES HORF — CE-2C.1 Orbital Classification

**Status:** CLOSED  
**Date:** 2026-08-31  
**Research line:** ACES HORF — Higher-Order Relations Framework  
**Scope:** pairwise-realizable relations on three binary variables

## 1. Result

Let

\[
R \subseteq Q_3=\{0,1\}^3
\]

be pairwise-realizable, i.e. every two-coordinate projection is the full \(\{0,1\}^2\). Let

\[
G=(\mathbb Z/2\mathbb Z)^3\rtimes S_3, \qquad |G|=48,
\]

act by independent bit complements and coordinate permutations.

Exhaustive classification gives exactly **35** pairwise-realizable relations:

\[
|R|=4:2,\quad |R|=5:8,\quad |R|=6:16,\quad |R|=7:8,\quad |R|=8:1.
\]

The 34 incomplete relations split into five \(G\)-orbits, of which four are non-affine.

\[
\boxed{|\Phi_3|=34}
\]

\[
\boxed{|\Phi_3/G|=5}
\]

\[
\boxed{|\Phi_{\mathrm{non-affine},3}|=32}
\]

\[
\boxed{|\Phi_{\mathrm{non-affine},3}/G|=4}
\]

The full relation \(Q_3\) is a separate singleton orbit.

## 2. Orbit decomposition

| Structural type | \(|R|\) | \(|H|\) | Forbidden-state geometry | Affine? | Orbit size |
|---|---:|---:|---|---|---:|
| AFFINE-PARITY | 4 | 4 | parity hyperplane | YES | 2 |
| N5-TRIANGLE | 5 | 3 | three holes, pairwise distance 2 | NO | 8 |
| N6-DIAGONAL | 6 | 2 | two holes, distance 2 | NO | 12 |
| N6-ANTIPODAL | 6 | 2 | two opposite holes, distance 3 | NO | 4 |
| N7-CO-SINGLETON | 7 | 1 | one forbidden vertex | NO | 8 |
| FULL | 8 | 0 | no forbidden vertices | — | 1 |

Check:

\[
2+8+12+4+8+1=35.
\]

Therefore the 32 non-affine relations are exactly

\[
\boxed{8+12+4+8=32}.
\]

## 3. Forbidden-state representation

Define

\[
H=Q_3\setminus R.
\]

For the non-affine classes, the geometry of \(H\) is:

- **N5:** three forbidden vertices with pairwise Hamming distance 2;
- **N6-D:** two forbidden vertices at Hamming distance 2;
- **N6-A:** two antipodal forbidden vertices at Hamming distance 3;
- **N7:** one forbidden vertex.

This converts the classification from a list of relations into a classification of forbidden-state configurations in the cube.

## 4. Affine boundary

For \(|R|=4\), pairwise realizability forces a functional dependency

\[
x_k=f(x_i,x_j),
\]

and the only possibilities are the two parity relations

\[
x_1\oplus x_2\oplus x_3=c,\qquad c\in\{0,1\}.
\]

Under the full cube symmetry group they form one structural affine family but two distinct \(G\)-orbits of size 2.

For every non-affine class \(|R|>4\), no coordinate is a deterministic function of the other two. Thus, in this minimal case,

\[
\boxed{\text{functional dependency}\iff\text{affine parity relation}.}
\]

## 5. Order versus mechanism

Every incomplete pairwise-realizable relation in this \(n=3\) case has order 3. Nevertheless, five structural realizations occur: one affine and four non-affine.

Hence

\[
\boxed{\text{same order}\not\Rightarrow\text{same mechanism}.}
\]

In particular,

\[
N6_D\neq N6_A,
\]

even though both have \(|R|=6\); their forbidden pairs have different Hamming distances.

## 6. Symmetry data

Orbit-stabilizer gives:

\[
\begin{array}{c|c|c}
\text{Orbit}&|O|&|\operatorname{Stab}_G|\\
\hline
AFFINE&2&24\\
N5&8&6\\
N6_D&12&4\\
N6_A&4&12\\
N7&8&6\\
FULL&1&48
\end{array}
\]

This supplies a second structural axis: residual symmetry / stabilizer size.

## 7. Theorem status

**CE-2C.1 is CLOSED as a finite classification theorem for \(n=3\).**

It does **not** yet establish a general theorem for arbitrary \(n\).

The next research question is therefore not another unrestricted enumeration. It is **CE-2C.2 — Mechanism Invariant Extraction**: determine whether forbidden-state geometry, projection-defect structure, distance spectrum, and symmetry provide a general invariant of higher-order constraint mechanisms.

## 8. Scaling boundary

The unrestricted relation space has size

\[
2^{2^n}.
\]

Thus:

\[
2^{2^3}=256,\qquad 2^{2^4}=65\,536,\qquad 2^{2^5}\approx4.3\times10^9.
\]

Brute-force enumeration therefore cannot be the long-term method. The research must transition from enumeration to structural invariants and predictive theory.

## 9. ACES relevance

CE-2C provides a minimal mathematical laboratory for the distinction

\[
\boxed{\text{local/pairwise consistency}\not\Rightarrow\text{global consistency}.}
\]

This is potentially relevant to ACES epistemic architecture: locally valid evidence does not by itself establish globally valid knowledge or a globally admissible state transition.

A possible future mapping is:

\[
Evidence
\rightarrow Local\ Consistency
\rightarrow Higher\text{-}Order\ Consistency
\rightarrow Epistemic\ Validation
\rightarrow Decision\ Authority
\rightarrow Verified\ State.
\]

This mapping is **research hypothesis only**, not an ACES canonical rule at this stage.

## 10. Long-term research objective

The broader target is a possible **Local-to-Global Constraint Theory**:

\[
\boxed{
\text{local observations}
\rightarrow
\text{constraints}
\rightarrow
\text{forbidden configurations}
\rightarrow
\text{global structure / obstruction}
}
\]

The decisive future test is whether the mechanism-invariant picture survives at \(n=4\) and beyond, and whether it yields a general predictive theorem rather than a sequence of finite classifications.

---

**Canonical status:** CE-2C.1 CLOSED.  
**No ACES architectural canon is claimed by this research artifact.**
