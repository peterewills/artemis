# Metrics for Graph Comparison: A Practitioner's Guide

**Authors:** Peter Wills and François G. Meyer (University of Colorado at Boulder)

## Abstract

This paper provides a comprehensive comparative study of distance measures for comparing graph structures. The authors evaluate commonly used graph metrics on their ability to discern between common topological features found in both random graph models and real-world networks. They introduce a multi-scale picture of graph structure and make recommendations for applying different distance measures to empirical data.

## Main Contribution

The primary contribution is a systematic evaluation of graph distance measures through:
1. Testing on prototypical random graph ensembles representing different structural features
2. Analyzing performance through a lens of global vs. local structure detection
3. Providing practical guidance on distance measure selection based on structural scales
4. Introducing the NetComp Python library implementing these distances

## Key Problem

Graph comparison is ubiquitous in:
- Neuroscience (brain network analysis)
- Cybersecurity (network intrusion detection)
- Social network analysis
- Bioinformatics (protein interaction networks)

The challenge is selecting appropriate distance measures that:
- Scale to large graphs (millions of vertices)
- Capture relevant structural features at different scales
- Provide meaningful comparisons for specific applications

## Technical Approach

### Distance Measure Categories

**1. Spectral Distances**
- Compare eigenvalue spectra of matrix representations
- Adjacency, Laplacian, and normalized Laplacian variants
- Do not require node correspondence
- Can focus on global (few eigenvalues) or multi-scale (many eigenvalues) features

**2. Matrix Distances**
- Compare pairwise node affinities organized in matrices
- Examples: Edit distance, resistance-perturbation distance, DeltaCon
- Require node correspondence
- Capture different connectivity patterns

**3. Feature-Based Distances**
- Compare specific graph features (degree distribution, clustering, etc.)
- Example: NetSimile
- Can be tailored to specific applications

### Multi-Scale Framework

The authors propose viewing graph structure at multiple scales:
- **Global structure**: Communities, hubs, overall connectivity patterns
- **Local structure**: Degree distributions, triangles, local clustering

Different distances are sensitive to different scales:
- Spectral distances using few eigenvalues → global structure
- Edit distance → local edge perturbations
- Resistance distance → connectivity changes at multiple scales

## Methodology

### Random Graph Ensembles

The authors test distances on prototypical models:
- Erdős-Rényi (random connections)
- Stochastic block models (community structure)
- Small-world networks
- Scale-free networks
- Random geometric graphs

### Evaluation Framework

1. **Contrast Statistic**: Measures ability to distinguish between graph ensembles
2. **Computational Efficiency**: All methods must scale linearly or near-linearly
3. **Empirical Validation**: Testing on real-world networks

## Key Findings

### Computational Complexity

| Distance | Complexity | Notes |
|----------|------------|-------|
| Spectral | O(n²) exact, O(n log² n) approx | Using randomized algorithms |
| Edit | O(n) | Simple edge counting |
| Resistance | O(n³) exact, O(n log² n) approx | Approximate versions practical |
| DeltaCon | O(n²) exact, O(n) approx | Fast belief propagation |
| NetSimile | O(n) | Feature computation dominates |

### Distance Performance

1. **Spectral distances**:
   - Excellent for detecting community structure changes
   - Flexible scale selection via eigenvalue truncation
   - Normalized Laplacian can compare different-sized graphs

2. **Matrix distances**:
   - Edit distance: Best for volume/density changes
   - Resistance distance: Sensitive to connectivity patterns
   - DeltaCon: Balances local and global features

3. **Feature-based**:
   - NetSimile: Highly customizable but feature-dependent
   - Computational constraints limit feature choices

## Practical Recommendations

### When to Use Each Distance

**Spectral Distances**:
- Community structure analysis
- Global topology changes
- When node correspondence unavailable
- Multi-scale analysis needed

**Edit Distance**:
- Simple edge addition/deletion detection
- When computational efficiency critical
- Local structure changes

**Resistance Distance**:
- Connectivity robustness analysis
- Path-based structure important
- Communication network analysis

**DeltaCon**:
- Information diffusion applications
- Need balance of scales
- Moderate-sized graphs

**NetSimile**:
- Domain-specific features important
- Interpretability required
- Custom feature sets available

## Technical Innovations

### Key Insights

1. **No universal best distance**: Choice depends on:
   - Structural features of interest
   - Computational constraints
   - Node correspondence availability

2. **Scale matters**: Distances capture different structural scales
   - Must match distance to analysis goals
   - Some distances inherently multi-scale

3. **Practical constraints**: Real-world applicability requires:
   - Linear/near-linear scaling
   - Robustness to noise
   - Interpretable results

### NetComp Library

The authors introduce a Python package implementing:
- All compared distance measures
- Efficient algorithms for large graphs
- Consistent API for easy comparison
- Integration with standard graph libraries

## Significance and Applications

### Theoretical Impact
- First comprehensive empirical comparison at scale
- Multi-scale framework for understanding distances
- Guidance on distance selection

### Practical Applications
- Network anomaly detection
- Temporal network analysis
- Graph classification tasks
- Change point detection in dynamic networks

## Future Directions

The authors suggest several extensions:
- Learning-based graph kernels
- Distances for graphs of different sizes (Wasserstein, Gromov-Hausdorff)
- Application-specific distance learning
- Integration with graph neural networks

## Conclusion

This work provides essential guidance for practitioners needing to compare graphs. By systematically evaluating distance measures on prototypical graph structures, the authors reveal that different distances excel at detecting different structural features. The multi-scale perspective and practical recommendations enable informed selection of appropriate distances for specific applications, while the NetComp library provides accessible implementations for immediate use.