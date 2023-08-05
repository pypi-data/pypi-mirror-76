use oxigraph::model::*;
use pyo3::basic::CompareOp;
use pyo3::exceptions::{IndexError, NotImplementedError, TypeError, ValueError};
use pyo3::prelude::*;
use pyo3::{PyIterProtocol, PyMappingProtocol, PyObjectProtocol};
use std::collections::hash_map::DefaultHasher;
use std::hash::Hash;
use std::hash::Hasher;
use std::vec::IntoIter;

/// An RDF `node identified by an IRI <https://www.w3.org/TR/rdf11-concepts/#dfn-iri>`_
///
/// :param value: the IRI as a string
/// :type value: str
/// :raises ValueError: if the IRI is not valid according to `RFC 3987 <https://tools.ietf.org/rfc/rfc3987>`_
///
/// The :py:func:`str` function provides a serialization compatible with NTriples, Turtle and SPARQL:
///
/// >>> str(NamedNode('http://example.com'))
/// '<http://example.com>'
#[pyclass(name = NamedNode)]
#[text_signature = "(value)"]
#[derive(Eq, PartialEq, Ord, PartialOrd, Debug, Clone, Hash)]
pub struct PyNamedNode {
    inner: NamedNode,
}

impl From<NamedNode> for PyNamedNode {
    fn from(inner: NamedNode) -> Self {
        Self { inner }
    }
}

impl From<PyNamedNode> for NamedNode {
    fn from(node: PyNamedNode) -> Self {
        node.inner
    }
}

impl From<PyNamedNode> for NamedOrBlankNode {
    fn from(node: PyNamedNode) -> Self {
        node.inner.into()
    }
}

impl From<PyNamedNode> for Term {
    fn from(node: PyNamedNode) -> Self {
        node.inner.into()
    }
}

impl From<PyNamedNode> for GraphName {
    fn from(node: PyNamedNode) -> Self {
        node.inner.into()
    }
}

#[pymethods]
impl PyNamedNode {
    #[new]
    fn new(value: String) -> PyResult<Self> {
        Ok(NamedNode::new(value)
            .map_err(|e| ValueError::py_err(e.to_string()))?
            .into())
    }

    /// :return: the named node IRI
    /// :rtype: str
    ///
    /// >>> NamedNode("http://example.com").value
    /// 'http://example.com'
    #[getter]
    fn value(&self) -> &str {
        self.inner.as_str()
    }
}

#[pyproto]
impl PyObjectProtocol for PyNamedNode {
    fn __str__(&self) -> String {
        self.inner.to_string()
    }

    fn __repr__(&self) -> String {
        let mut buffer = String::new();
        named_node_repr(self.inner.as_ref(), &mut buffer);
        buffer
    }

    fn __hash__(&self) -> u64 {
        hash(&self.inner)
    }

    fn __richcmp__(&self, other: &PyCell<Self>, op: CompareOp) -> bool {
        eq_ord_compare(self, &other.borrow(), op)
    }
}

/// An RDF `blank node <https://www.w3.org/TR/rdf11-concepts/#dfn-blank-node>`_
///
/// :param value: the `blank node ID <https://www.w3.org/TR/rdf11-concepts/#dfn-blank-node-identifier>`_ (if not present, a random blank node ID is automatically generated).
/// :type value: str, optional
///
/// The :py:func:`str` function provides a serialization compatible with NTriples, Turtle and SPARQL:
///
/// >>> str(BlankNode('ex'))
/// '_:ex'
#[pyclass(name = BlankNode)]
#[text_signature = "(value)"]
#[derive(Eq, PartialEq, Debug, Clone, Hash)]
pub struct PyBlankNode {
    inner: BlankNode,
}

impl From<BlankNode> for PyBlankNode {
    fn from(inner: BlankNode) -> Self {
        Self { inner }
    }
}

impl From<PyBlankNode> for BlankNode {
    fn from(node: PyBlankNode) -> Self {
        node.inner
    }
}

impl From<PyBlankNode> for NamedOrBlankNode {
    fn from(node: PyBlankNode) -> Self {
        node.inner.into()
    }
}

impl From<PyBlankNode> for Term {
    fn from(node: PyBlankNode) -> Self {
        node.inner.into()
    }
}

impl From<PyBlankNode> for GraphName {
    fn from(node: PyBlankNode) -> Self {
        node.inner.into()
    }
}

#[pymethods]
impl PyBlankNode {
    #[new]
    fn new(value: Option<String>) -> PyResult<Self> {
        Ok(if let Some(value) = value {
            BlankNode::new(value).map_err(|e| ValueError::py_err(e.to_string()))?
        } else {
            BlankNode::default()
        }
        .into())
    }

    /// :return: the `blank node ID <https://www.w3.org/TR/rdf11-concepts/#dfn-blank-node-identifier>`_
    /// :rtype: str
    ///
    /// >>> BlankNode("ex").value
    /// 'ex'
    #[getter]
    fn value(&self) -> &str {
        self.inner.as_str()
    }
}

#[pyproto]
impl PyObjectProtocol for PyBlankNode {
    fn __str__(&self) -> String {
        self.inner.to_string()
    }

    fn __repr__(&self) -> String {
        let mut buffer = String::new();
        blank_node_repr(self.inner.as_ref(), &mut buffer);
        buffer
    }

    fn __hash__(&self) -> u64 {
        hash(&self.inner)
    }

    fn __richcmp__(&self, other: &PyCell<Self>, op: CompareOp) -> PyResult<bool> {
        eq_compare(self, &other.borrow(), op)
    }
}

/// An RDF `literal <https://www.w3.org/TR/rdf11-concepts/#dfn-literal>`_
///
/// :param value: the literal value or `lexical form <https://www.w3.org/TR/rdf11-concepts/#dfn-lexical-form>`_
/// :type value: str
/// :param datatype: the literal `datatype IRI <https://www.w3.org/TR/rdf11-concepts/#dfn-datatype-iri>`_.
/// :type datatype: NamedNode, optional
/// :param language: the literal `language tag <https://www.w3.org/TR/rdf11-concepts/#dfn-language-tag>`_
/// :type language: str, optional
/// :raises ValueError: if the language tag is not valid according to `RFC 5646 <https://tools.ietf.org/rfc/rfc5646>`_ (`BCP 47 <https://tools.ietf.org/rfc/bcp/bcp47>`_)
///
/// The :py:func:`str` function provides a serialization compatible with NTriples, Turtle and SPARQL:
///
/// >>> str(Literal('example'))
/// '"example"'
/// >>> str(Literal('example', language='en'))
/// '"example"@en'
/// >>> str(Literal('11', datatype=NamedNode('http://www.w3.org/2001/XMLSchema#integer')))
/// '"11"^^<http://www.w3.org/2001/XMLSchema#integer>'
#[pyclass(name = Literal)]
#[text_signature = "(value, *, datatype = None, language = None)"]
#[derive(Eq, PartialEq, Debug, Clone, Hash)]
pub struct PyLiteral {
    inner: Literal,
}

impl From<Literal> for PyLiteral {
    fn from(inner: Literal) -> Self {
        Self { inner }
    }
}

impl From<PyLiteral> for Literal {
    fn from(literal: PyLiteral) -> Self {
        literal.inner
    }
}

impl From<PyLiteral> for Term {
    fn from(node: PyLiteral) -> Self {
        node.inner.into()
    }
}

#[pymethods]
impl PyLiteral {
    #[new]
    #[args(value, "*", datatype = "None", language = "None")]
    fn new(
        value: String,
        language: Option<String>,
        datatype: Option<PyNamedNode>,
    ) -> PyResult<Self> {
        Ok(if let Some(language) = language {
            if let Some(datatype) = datatype {
                if datatype.value() != "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString" {
                    return Err(ValueError::py_err(
                        "The literals with a language tag must use the rdf:langString datatype",
                    ));
                }
            }
            Literal::new_language_tagged_literal(value, language)
                .map_err(|e| ValueError::py_err(e.to_string()))?
        } else if let Some(datatype) = datatype {
            Literal::new_typed_literal(value, datatype)
        } else {
            Literal::new_simple_literal(value)
        }
        .into())
    }

    /// :return: the literal value or `lexical form <https://www.w3.org/TR/rdf11-concepts/#dfn-lexical-form>`_
    /// :rtype: str
    ///
    /// >>> Literal("example").value
    /// 'example'
    #[getter]
    fn value(&self) -> &str {
        self.inner.value()
    }

    /// :return: the literal `language tag <https://www.w3.org/TR/rdf11-concepts/#dfn-language-tag>`_
    /// :rtype: str or None
    ///
    /// >>> Literal('example', language='en').language
    /// 'en'
    /// >>> Literal('example').language
    ///
    #[getter]
    fn language(&self) -> Option<&str> {
        self.inner.language()
    }

    /// :return: the literal `datatype IRI <https://www.w3.org/TR/rdf11-concepts/#dfn-datatype-iri>`_
    /// :rtype: NamedNode
    ///
    /// >>> Literal('11', datatype=NamedNode('http://www.w3.org/2001/XMLSchema#integer')).datatype
    /// <NamedNode value=http://www.w3.org/2001/XMLSchema#integer>
    /// >>> Literal('example').datatype
    /// <NamedNode value=http://www.w3.org/2001/XMLSchema#string>
    /// >>> Literal('example', language='en').datatype
    /// <NamedNode value=http://www.w3.org/1999/02/22-rdf-syntax-ns#langString>
    #[getter]
    fn datatype(&self) -> PyNamedNode {
        self.inner.datatype().into_owned().into()
    }
}

#[pyproto]
impl PyObjectProtocol for PyLiteral {
    fn __str__(&self) -> String {
        self.inner.to_string()
    }

    fn __repr__(&self) -> String {
        let mut buffer = String::new();
        literal_repr(self.inner.as_ref(), &mut buffer);
        buffer
    }

    fn __hash__(&self) -> u64 {
        hash(&self.inner)
    }

    fn __richcmp__(&self, other: &PyCell<Self>, op: CompareOp) -> PyResult<bool> {
        eq_compare(self, &other.borrow(), op)
    }
}

/// The RDF `default graph name <https://www.w3.org/TR/rdf11-concepts/#dfn-default-graph>`_
#[pyclass(name = DefaultGraph)]
#[derive(Eq, PartialEq, Debug, Clone, Copy, Hash)]
pub struct PyDefaultGraph {}

impl From<PyDefaultGraph> for GraphName {
    fn from(_: PyDefaultGraph) -> Self {
        GraphName::DefaultGraph
    }
}

#[pymethods]
impl PyDefaultGraph {
    #[new]
    fn new() -> Self {
        PyDefaultGraph {}
    }

    #[getter]
    fn value(&self) -> &str {
        ""
    }
}

#[pyproto]
impl PyObjectProtocol for PyDefaultGraph {
    fn __str__(&self) -> &'p str {
        "DEFAULT"
    }

    fn __repr__(&self) -> &'p str {
        "<DefaultGraph>"
    }

    fn __hash__(&self) -> u64 {
        0
    }

    fn __richcmp__(&self, other: &PyCell<Self>, op: CompareOp) -> PyResult<bool> {
        eq_compare(self, &other.borrow(), op)
    }
}

/// An RDF `triple <https://www.w3.org/TR/rdf11-concepts/#dfn-rdf-triple>`_
///
/// :param subject: the triple subject
/// :type subject: NamedNode or BlankNode
/// :param predicate: the triple predicate
/// :type predicate: NamedNode
/// :param object: the triple object
/// :type object: NamedNode or BlankNode or Literal
///
/// The :py:func:`str` function provides a serialization compatible with NTriples, Turtle and SPARQL:
///
/// >>> str(Triple(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1')))
/// '<http://example.com> <http://example.com/p> "1" .'
///
/// A triple could also be easily destructed into its components:
///
/// >>> (s, p, o) = Triple(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'))
#[pyclass(name = Triple)]
#[derive(Eq, PartialEq, Debug, Clone, Hash)]
#[text_signature = "(subject, predicate, object)"]
pub struct PyTriple {
    inner: Triple,
}

impl From<Triple> for PyTriple {
    fn from(inner: Triple) -> Self {
        Self { inner }
    }
}

impl From<PyTriple> for Triple {
    fn from(node: PyTriple) -> Self {
        node.inner
    }
}

impl<'a> From<&'a PyTriple> for TripleRef<'a> {
    fn from(node: &'a PyTriple) -> Self {
        node.inner.as_ref()
    }
}

#[pymethods]
impl PyTriple {
    #[new]
    fn new(subject: &PyAny, predicate: &PyAny, object: &PyAny) -> PyResult<Self> {
        Ok(Triple::new(
            extract_named_or_blank_node(subject)?,
            extract_named_node(predicate)?,
            extract_term(object)?,
        )
        .into())
    }

    /// :return: the triple subject
    /// :rtype: NamedNode or BlankNode
    ///
    /// >>> Triple(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1')).subject
    /// <NamedNode value=http://example.com>
    #[getter]
    fn subject(&self, py: Python<'_>) -> PyObject {
        named_or_blank_node_to_python(py, self.inner.subject.clone())
    }

    /// :return: the triple predicate
    /// :rtype: NamedNode
    ///
    /// >>> Triple(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1')).predicate
    /// <NamedNode value=http://example.com/p>
    #[getter]
    fn predicate(&self) -> PyNamedNode {
        self.inner.predicate.clone().into()
    }

    /// :return: the triple object
    /// :rtype: NamedNode or BlankNode or Literal
    ///
    /// >>> Triple(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1')).object
    /// <Literal value=1 datatype=<NamedNode value=http://www.w3.org/2001/XMLSchema#string>>
    #[getter]
    fn object(&self, py: Python<'_>) -> PyObject {
        term_to_python(py, self.inner.object.clone())
    }
}

#[pyproto]
impl PyObjectProtocol for PyTriple {
    fn __str__(&self) -> String {
        self.inner.to_string()
    }

    fn __repr__(&self) -> String {
        let mut buffer = String::new();
        buffer.push_str("<Triple subject=");
        term_repr(self.inner.subject.as_ref().into(), &mut buffer);
        buffer.push_str(" predicate=");
        named_node_repr(self.inner.predicate.as_ref(), &mut buffer);
        buffer.push_str(" object=");
        term_repr(self.inner.object.as_ref(), &mut buffer);
        buffer.push('>');
        buffer
    }

    fn __hash__(&self) -> u64 {
        hash(&self.inner)
    }

    fn __richcmp__(&self, other: &PyCell<Self>, op: CompareOp) -> PyResult<bool> {
        eq_compare(self, &other.borrow(), op)
    }
}

#[pyproto]
impl PyMappingProtocol<'p> for PyTriple {
    fn __len__(&self) -> usize {
        3
    }

    fn __getitem__(&self, input: usize) -> PyResult<PyObject> {
        let gil = Python::acquire_gil();
        match input {
            0 => Ok(named_or_blank_node_to_python(
                gil.python(),
                self.inner.subject.clone(),
            )),
            1 => Ok(PyNamedNode::from(self.inner.predicate.clone()).into_py(gil.python())),
            2 => Ok(term_to_python(gil.python(), self.inner.object.clone())),
            _ => Err(IndexError::py_err("A triple has only 3 elements")),
        }
    }
}

#[pyproto]
impl PyIterProtocol for PyTriple {
    fn __iter__(slf: PyRef<Self>) -> TripleComponentsIter {
        TripleComponentsIter {
            inner: vec![
                slf.inner.subject.clone().into(),
                slf.inner.predicate.clone().into(),
                slf.inner.object.clone(),
            ]
            .into_iter(),
        }
    }
}

/// An RDF `triple <https://www.w3.org/TR/rdf11-concepts/#dfn-rdf-triple>`_
/// in a `RDF dataset <https://www.w3.org/TR/rdf11-concepts/#dfn-rdf-dataset>`_
///
/// :param subject: the quad subject
/// :type subject: NamedNode or BlankNode
/// :param predicate: the quad predicate
/// :type predicate: NamedNode
/// :param object: the quad object
/// :type object: NamedNode or BlankNode or Literal
/// :param graph: the quad graph name. If not present, the default graph is assumed.
/// :type object: NamedNode or BlankNode or DefaultGraph or None
///
/// The :py:func:`str` function provides a serialization compatible with NTriples, Turtle and SPARQL:
///
/// >>> str(Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g')))
/// '<http://example.com> <http://example.com/p> "1" <http://example.com/g> .'
///
/// >>> str(Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), DefaultGraph()))
/// '<http://example.com> <http://example.com/p> "1" .'
///
/// A quad could also be easily destructed into its components:
///
/// >>> (s, p, o, g) = Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g'))
#[pyclass(name = Quad)]
#[text_signature = "(subject, predicate, object, graph_name = None)"]
#[derive(Eq, PartialEq, Debug, Clone, Hash)]
pub struct PyQuad {
    inner: Quad,
}

impl From<Quad> for PyQuad {
    fn from(inner: Quad) -> Self {
        Self { inner }
    }
}

impl From<PyQuad> for Quad {
    fn from(node: PyQuad) -> Self {
        node.inner
    }
}

impl<'a> From<&'a PyQuad> for QuadRef<'a> {
    fn from(node: &'a PyQuad) -> Self {
        node.inner.as_ref()
    }
}

#[pymethods]
impl PyQuad {
    #[new]
    fn new(
        subject: &PyAny,
        predicate: &PyAny,
        object: &PyAny,
        graph_name: Option<&PyAny>,
    ) -> PyResult<Self> {
        Ok(Quad::new(
            extract_named_or_blank_node(subject)?,
            extract_named_node(predicate)?,
            extract_term(object)?,
            if let Some(graph_name) = graph_name {
                extract_graph_name(graph_name)?
            } else {
                GraphName::DefaultGraph
            },
        )
        .into())
    }

    /// :return: the quad subject
    /// :rtype: NamedNode or BlankNode
    ///
    /// >>> Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g')).subject
    /// <NamedNode value=http://example.com>
    #[getter]
    fn subject(&self, py: Python<'_>) -> PyObject {
        named_or_blank_node_to_python(py, self.inner.subject.clone())
    }

    /// :return: the quad predicate
    /// :rtype: NamedNode
    ///
    /// >>> Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g')).predicate
    /// <NamedNode value=http://example.com/p>
    #[getter]
    fn predicate(&self) -> PyNamedNode {
        self.inner.predicate.clone().into()
    }

    /// :return: the quad object
    /// :rtype: NamedNode or BlankNode or Literal
    ///
    /// >>> Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g')).object
    /// <Literal value=1 datatype=<NamedNode value=http://www.w3.org/2001/XMLSchema#string>>
    #[getter]
    fn object(&self, py: Python<'_>) -> PyObject {
        term_to_python(py, self.inner.object.clone())
    }

    /// :return: the quad graph name
    /// :rtype: NamedNode or BlankNode or DefaultGraph
    ///
    /// >>> Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g')).graph_name
    /// <NamedNode value=http://example.com/g>
    #[getter]
    fn graph_name(&self, py: Python<'_>) -> PyObject {
        graph_name_to_python(py, self.inner.graph_name.clone())
    }

    /// :return: the quad underlying triple
    /// :rtype: Triple
    ///
    /// >>> Quad(NamedNode('http://example.com'), NamedNode('http://example.com/p'), Literal('1'), NamedNode('http://example.com/g')).triple
    /// <Triple subject=<NamedNode value=http://example.com> predicate=<NamedNode value=http://example.com/p> object=<Literal value=1 datatype=<NamedNode value=http://www.w3.org/2001/XMLSchema#string>>>
    #[getter]
    fn triple(&self) -> PyTriple {
        Triple::from(self.inner.clone()).into()
    }
}

#[pyproto]
impl PyObjectProtocol for PyQuad {
    fn __str__(&self) -> String {
        self.inner.to_string()
    }

    fn __repr__(&self) -> String {
        let mut buffer = String::new();
        buffer.push_str("<Quad subject=");
        term_repr(self.inner.subject.as_ref().into(), &mut buffer);
        buffer.push_str(" predicate=");
        named_node_repr(self.inner.predicate.as_ref(), &mut buffer);
        buffer.push_str(" object=");
        term_repr(self.inner.object.as_ref(), &mut buffer);
        buffer.push_str(" graph_name=");
        graph_name_repr(self.inner.graph_name.as_ref(), &mut buffer);
        buffer.push('>');
        buffer
    }

    fn __hash__(&self) -> u64 {
        hash(&self.inner)
    }

    fn __richcmp__(&self, other: &PyCell<Self>, op: CompareOp) -> PyResult<bool> {
        eq_compare(self, &other.borrow(), op)
    }
}

#[pyproto]
impl PyMappingProtocol<'p> for PyQuad {
    fn __len__(&self) -> usize {
        4
    }

    fn __getitem__(&self, input: usize) -> PyResult<PyObject> {
        let gil = Python::acquire_gil();
        match input {
            0 => Ok(named_or_blank_node_to_python(
                gil.python(),
                self.inner.subject.clone(),
            )),
            1 => Ok(PyNamedNode::from(self.inner.predicate.clone()).into_py(gil.python())),
            2 => Ok(term_to_python(gil.python(), self.inner.object.clone())),
            3 => Ok(graph_name_to_python(
                gil.python(),
                self.inner.graph_name.clone(),
            )),
            _ => Err(IndexError::py_err("A quad has only 4 elements")),
        }
    }
}

#[pyproto]
impl PyIterProtocol for PyQuad {
    fn __iter__(slf: PyRef<Self>) -> QuadComponentsIter {
        QuadComponentsIter {
            inner: vec![
                Some(slf.inner.subject.clone().into()),
                Some(slf.inner.predicate.clone().into()),
                Some(slf.inner.object.clone()),
                match slf.inner.graph_name.clone() {
                    GraphName::NamedNode(node) => Some(node.into()),
                    GraphName::BlankNode(node) => Some(node.into()),
                    GraphName::DefaultGraph => None,
                },
            ]
            .into_iter(),
        }
    }
}

pub fn extract_named_node(py: &PyAny) -> PyResult<NamedNode> {
    if let Ok(node) = py.downcast::<PyCell<PyNamedNode>>() {
        Ok(node.borrow().clone().into())
    } else {
        Err(TypeError::py_err(format!(
            "{} is not an RDF named node",
            py.get_type().name(),
        )))
    }
}

pub fn extract_named_or_blank_node(py: &PyAny) -> PyResult<NamedOrBlankNode> {
    if let Ok(node) = py.downcast::<PyCell<PyNamedNode>>() {
        Ok(node.borrow().clone().into())
    } else if let Ok(node) = py.downcast::<PyCell<PyBlankNode>>() {
        Ok(node.borrow().clone().into())
    } else {
        Err(TypeError::py_err(format!(
            "{} is not an RDF named or blank node",
            py.get_type().name(),
        )))
    }
}

pub fn named_or_blank_node_to_python(py: Python<'_>, node: NamedOrBlankNode) -> PyObject {
    match node {
        NamedOrBlankNode::NamedNode(node) => PyNamedNode::from(node).into_py(py),
        NamedOrBlankNode::BlankNode(node) => PyBlankNode::from(node).into_py(py),
    }
}

pub fn extract_term(py: &PyAny) -> PyResult<Term> {
    if let Ok(node) = py.downcast::<PyCell<PyNamedNode>>() {
        Ok(node.borrow().clone().into())
    } else if let Ok(node) = py.downcast::<PyCell<PyBlankNode>>() {
        Ok(node.borrow().clone().into())
    } else if let Ok(literal) = py.downcast::<PyCell<PyLiteral>>() {
        Ok(literal.borrow().clone().into())
    } else {
        Err(TypeError::py_err(format!(
            "{} is not an RDF named or blank node",
            py.get_type().name(),
        )))
    }
}

pub fn term_to_python(py: Python<'_>, term: Term) -> PyObject {
    match term {
        Term::NamedNode(node) => PyNamedNode::from(node).into_py(py),
        Term::BlankNode(node) => PyBlankNode::from(node).into_py(py),
        Term::Literal(literal) => PyLiteral::from(literal).into_py(py),
    }
}

pub fn extract_graph_name(py: &PyAny) -> PyResult<GraphName> {
    if let Ok(node) = py.downcast::<PyCell<PyNamedNode>>() {
        Ok(node.borrow().clone().into())
    } else if let Ok(node) = py.downcast::<PyCell<PyBlankNode>>() {
        Ok(node.borrow().clone().into())
    } else if let Ok(node) = py.downcast::<PyCell<PyDefaultGraph>>() {
        Ok(node.borrow().clone().into())
    } else {
        Err(TypeError::py_err(format!(
            "{} is not a valid RDF graph name",
            py.get_type().name(),
        )))
    }
}

pub fn graph_name_to_python(py: Python<'_>, name: GraphName) -> PyObject {
    match name {
        GraphName::NamedNode(node) => PyNamedNode::from(node).into_py(py),
        GraphName::BlankNode(node) => PyBlankNode::from(node).into_py(py),
        GraphName::DefaultGraph => PyDefaultGraph::new().into_py(py),
    }
}

fn eq_compare<T: Eq>(a: &T, b: &T, op: CompareOp) -> PyResult<bool> {
    match op {
        CompareOp::Eq => Ok(a == b),
        CompareOp::Ne => Ok(a != b),
        _ => Err(NotImplementedError::py_err("Ordering is not implemented")),
    }
}

fn eq_ord_compare<T: Eq + Ord>(a: &T, b: &T, op: CompareOp) -> bool {
    match op {
        CompareOp::Lt => a < b,
        CompareOp::Le => a <= b,
        CompareOp::Eq => a == b,
        CompareOp::Ne => a != b,
        CompareOp::Gt => a > b,
        CompareOp::Ge => a >= b,
    }
}

fn hash(t: &impl Hash) -> u64 {
    let mut s = DefaultHasher::new();
    t.hash(&mut s);
    s.finish()
}

fn named_node_repr(node: NamedNodeRef<'_>, buffer: &mut String) {
    buffer.push_str("<NamedNode value=");
    buffer.push_str(node.as_str());
    buffer.push('>');
}

fn blank_node_repr(node: BlankNodeRef<'_>, buffer: &mut String) {
    buffer.push_str("<BlankNode value=");
    buffer.push_str(node.as_str());
    buffer.push('>');
}

fn literal_repr(literal: LiteralRef<'_>, buffer: &mut String) {
    buffer.push_str("<Literal value=");
    buffer.push_str(literal.value());
    if let Some(language) = literal.language() {
        buffer.push_str(" language=");
        buffer.push_str(language);
    } else {
        buffer.push_str(" datatype=");
        named_node_repr(literal.datatype(), buffer);
    }
    buffer.push('>');
}

pub fn term_repr(term: TermRef<'_>, buffer: &mut String) {
    match term {
        TermRef::NamedNode(node) => named_node_repr(node, buffer),
        TermRef::BlankNode(node) => blank_node_repr(node, buffer),
        TermRef::Literal(literal) => literal_repr(literal, buffer),
    }
}

fn graph_name_repr(term: GraphNameRef<'_>, buffer: &mut String) {
    match term {
        GraphNameRef::NamedNode(node) => named_node_repr(node, buffer),
        GraphNameRef::BlankNode(node) => blank_node_repr(node, buffer),
        GraphNameRef::DefaultGraph => buffer.push_str("<DefaultGraph>"),
    }
}

#[pyclass(unsendable)]
pub struct TripleComponentsIter {
    inner: IntoIter<Term>,
}

#[pyproto]
impl PyIterProtocol for TripleComponentsIter {
    fn __iter__(slf: PyRefMut<Self>) -> Py<Self> {
        slf.into()
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<PyObject> {
        slf.inner.next().map(move |t| term_to_python(slf.py(), t))
    }
}

#[pyclass(unsendable)]
pub struct QuadComponentsIter {
    inner: IntoIter<Option<Term>>,
}

#[pyproto]
impl PyIterProtocol for QuadComponentsIter {
    fn __iter__(slf: PyRefMut<Self>) -> Py<Self> {
        slf.into()
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<PyObject> {
        slf.inner.next().map(move |t| {
            if let Some(t) = t {
                term_to_python(slf.py(), t)
            } else {
                PyDefaultGraph {}.into_py(slf.py())
            }
        })
    }
}
