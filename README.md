# Fractured Pane Graph Generator

Fractured Panes are a way of visualizing hierarchical information. Conceptually they work similarly to a tree map with a key difference being the rotation of each slice as the hierarchy is constructed changes to allow for easier visualization of the belongings of sets. The fundamental feature that distinguishes Fractured Panes from treemaps and their alternatives is that Fractured Panes, relying on slices for their visualization, exclusively render data organized as a differential ontology.

## What is a Differential Ontology?
While there is currently no code overlap, Fractured Panes are intended to be a companion piece to my project on [Coils](https://github.com/ap0phasi/neuralcoil), which are a means of representing dynamics within a differential ontology. In that project I go into much more detail on the philosophical underpinnings of differential ontology, but for our purposes here we can establish some simple rules for slicing up reality.

### Perpetual Exclusion:
In our formalism for differential ontology, all concepts are treated as a slice, as a representation of "this" and "not-this". Neither possesses it's own means of existence, they are made so by each other. As such, the presentation of any concept is concomitant with it's exclusion. This is different than establishing a dichotomy, because if we wish to present the concepts of art and science, we must present "science/not-science", and then slice "not-science" into the presentation of "art/not-art". Every concept has its exclusion, there is always something left out.

### Presentations of the Void:
We now must ask what is the fundamental, parent concept we are slicing? What is the presentation that is not differentiated so that we might differentiate it? According to Perpetual Exclusion, every concept is a product of differentiation, so there can be no undifferentiated concept. The answer to our question is a void, so that is what we will be slicing. All concepts are presentations of the void.

This sounds like philosophical posturing, and it is, but it has some impact on our practical implementation. Formally, we can't "start" with a monad, some all encompassing parent concept, instead we must always start with the void. As concepts are presentations of the void, there do not exist inherent properties hidden within the concepts that individuate them and make them fundamental or possessing their own means of existence. A concept is made so by how it interfaces with other concepts.

# Usage and Methodology

To generate a fractured pane for interconnected concepts, we first create a dataframe of the concepts such as:

```
belongings = [
    {"parent": "Science", "concept": "Physics"},
    {"parent": "Physics", "concept": "Quantum Mechanics"},
    {"parent": "Physics", "concept": "Relativity"},
    {"parent": "Relativity", "concept": "General Relativity"},
    {'parent': "Art", "concept": "Watercolor"},
    {'parent': "Art", "concept": "Ceramics"},
    {'parent': "Watercolor", "concept": "Wet-On-Dry"},
    {'parent': "Watercolor", "concept": "Dry-On-Dry"}
    # ... you can add more belongings here
]
```
We then use the provided helper functions to create a differential ontology, assigning a binary encoding to each concept:

```
 # Convert belongings to DataFrame
belongings_df = pd.DataFrame(belongings)

belongings_df = prepare_belonging_df(belongings_df)

df = generate_ontology_tree(belongings_df)
```

Now from our encoded ontology we can generate a Fractured Pane:

```
resulting_polygons = slice_space(df)

plotly_polygons(resulting_polygons)
```

This will generate an interactive plotly graphic showing our Fractured Pane:

![Demo](https://github.com/ap0phasi/FracturedPanePy/blob/main/media/FracturedPane_example.gif)

By default, unnamed concepts will not be rendered, allowing for us to see the layering of concepts with slices. 

# Future Developments
I have a number of developments planned that will offer some integration with my other projects. 

## Graph Optimization:
Currently the size and orientation of the resulting fragments in the Fractured Pane are not significant, but through graph optimization I would like to make it so the size and location are meaningful. In a Fractured Pane concepts could belong to different parents but "touch" each other on the plot. I would like to use this to represent the interrelationship and influence of concepts with different parents. I am eager to see if my [Scedastic Surrogate Swarm optimizer](https://github.com/ap0phasi/ScedasticSurrogateSwarmPy) is up for the task. Optimization of these graphs will be essential for visualization of Coil dynamics.

## Automate Differential Ontology:
Another related project I am planning is chaining LLMs to automatically extract concepts from text and construct belonging networks. These can be passed to the Fractured Pane procedure for full automation of differential ontologies.

## Use Fractured Pane as Transformer Context:
Once Fractured Pane graph generation is optimized to better represent relationships, it will be interesting to provide these Fractured Panes as context for a transformer model. As the Fractured Pane is a 2D image where the colors are derived from the binary encodings, it is a good candidate for a CNN-based transformers.

Relatedly, the automated ontology procedure could be applied to the features of a timeseries, where the constructed ontology could be passed as a context to a model like my [CerberusTS](https://github.com/ap0phasi/cerberusR) project.

## Performance and Porting:
The Fractured Pane Python script is currently meant as a proof of concept and a grounds for research, and as such has not been optimized for performance. Once the methodology firms up I will start porting into javascript to allow for applications such as visualizing in a Vue dashboard.

## Flexible Ancestry:
Currently the expectation for our ```belongings``` dataframe is that each concept is only provided with one parent, therefore each concept only appears once. In cases where a concept is duplicated, the duplicates are dropped by the current scripts. I will investigate ways to have a more flexible "ancestry" where concepts belong to multiple parents. 