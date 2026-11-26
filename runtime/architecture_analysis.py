"""Native contract-relative architecture-analysis semantic core."""
from __future__ import annotations
from typing import Any, Callable, Mapping, Iterable

# I. Architecture contract and input normalization.
REQUIRED_OUTPUTS=(
    "ArchClass","Violations","LocalizationFamilies","DependencyState",
    "InteractionState","TransformationFrontier","SuccessorFrontier",
    "Coverage","OpenConflictBlocked","Provenance",
)

UNIT_JOB_PURITY="UNIT_JOB_PURITY"


def _normalized_jobs(value:Any)->tuple[str,...]:
    if value is None:
        return ()
    if isinstance(value,str):
        return (value,) if value else ()
    if isinstance(value, Mapping):
        raise ValueError("UNIT_JOB_IDENTITIES_REQUIRED")
    try:
        jobs=tuple(value)
    except TypeError as exc:
        raise ValueError("UNIT_JOB_IDENTITIES_REQUIRED") from exc
    if any(not isinstance(job,str) for job in jobs):
        raise ValueError("UNIT_JOB_IDENTITIES_REQUIRED")
    return tuple(dict.fromkeys(job for job in jobs if job))

def _unit_ids(value:Any)->set[str]:
    if not isinstance(value,(list,tuple,set,frozenset)) or any(
        not isinstance(x,str) or not x.strip() for x in value
    ):
        raise ValueError("UNIT_ID_COLLECTION_REQUIRED")
    return set(value)


# II. Schema-neutral graph diagnostics.
def declared_dependency_paths(dependencies, *, roots=None):
    """Shortest deterministic path witnesses within a finite declared graph.

    Edges point from a consumer to its dependency. Missing targets are not
    traversed; a path is a possible channel, not causal or execution evidence.
    Self-reachability is left to the separate cyclic-components diagnostic.
    Supply roots to bound the search; omitted roots request all declared nodes.
    """
    from collections import deque

    selected = set(dependencies) if roots is None else set(roots)
    if not selected <= dependencies.keys():
        raise ValueError("ARCHITECTURE_PATH_ROOT_NOT_DECLARED")
    paths = {}
    for start in sorted(selected):
        witnesses = {start: [start]}
        pending = deque([start])
        while pending:
            node = pending.popleft()
            for target in sorted(set(dependencies[node])):
                if target not in dependencies or target in witnesses:
                    continue
                witnesses[target] = witnesses[node] + [target]
                pending.append(target)
        del witnesses[start]
        paths[start] = witnesses
    return paths


def cyclic_components(dependencies):
    """Return deterministic cyclic SCCs, including self-loops.

    Iterative Kosaraju traversal avoids recursion limits and computes graph
    components in O(V + E) before output sorting. Dangling targets are ignored;
    these components describe declared links, not causal dependencies.
    """
    graph = {node: tuple(target for target in targets if target in dependencies)
             for node, targets in dependencies.items()}
    reverse = {node: [] for node in graph}
    for node, targets in graph.items():
        for target in targets:
            reverse[target].append(node)

    visited = set()
    finished = []
    for start in graph:
        if start in visited:
            continue
        visited.add(start)
        stack = [(start, iter(graph[start]))]
        while stack:
            node, targets = stack[-1]
            try:
                target = next(targets)
            except StopIteration:
                stack.pop()
                finished.append(node)
                continue
            if target not in visited:
                visited.add(target)
                stack.append((target, iter(graph[target])))

    visited.clear()
    components = []
    for start in reversed(finished):
        if start in visited:
            continue
        visited.add(start)
        pending = [start]
        component = []
        while pending:
            node = pending.pop()
            component.append(node)
            for target in reverse[node]:
                if target not in visited:
                    visited.add(target)
                    pending.append(target)
        if len(component) > 1 or start in graph[start]:
            components.append(sorted(component))
    return sorted(components)


def static_source_relationships(sources):
    """Extract bounded explicit references between exact selected source paths.

    Python import-name matches are possible channels, not proof of resolution
    or execution. Markdown covers simple relative inline links only. Missing
    references, dynamic imports and semantic dependencies remain uncertified.
    """
    import ast
    import posixpath
    import re
    from urllib.parse import unquote, urlsplit

    paths=set(sources)
    modules={}
    for path in paths:
        if path.endswith('.py'):
            name=path[:-3].replace('/','.')
            for alias in {name,name.rsplit('.',1)[-1]}:
                modules.setdefault(alias,set()).add(path)
    references=[]
    unresolved=[]
    for path,body in sorted(sources.items()):
        if path.endswith('.py'):
            try:
                tree=ast.parse(body,filename=path)
            except SyntaxError as exc:
                unresolved.append({'source':path,'reason':'PYTHON_PARSE_FAILED','line':exc.lineno})
                continue
            for node in ast.walk(tree):
                if isinstance(node,ast.Import):
                    names=[alias.name for alias in node.names]
                elif isinstance(node,ast.ImportFrom) and node.level==0 and node.module:
                    names=[node.module]
                else:
                    continue
                for name in names:
                    targets=modules.get(name,set())
                    if len(targets)==1:
                        references.append({'source':path,'target':next(iter(targets)),
                            'kind':'PYTHON_IMPORT_NAME_MATCH','line':node.lineno,'token':name})
                    elif len(targets)>1:
                        unresolved.append({'source':path,'reason':'AMBIGUOUS_IMPORT_NAME',
                                           'line':node.lineno,'token':name,'candidates':sorted(targets)})
        elif path.lower().endswith(('.md','.markdown')):
            fence=None
            for lineno,line in enumerate(body.splitlines(),1):
                fence_match=re.match(r'^\s{0,3}([\x60~]{3,})',line)
                if fence_match and len(set(fence_match.group(1)))==1:
                    marker=fence_match.group(1)
                    if fence is None:
                        fence=marker
                    elif marker[0]==fence[0] and len(marker)>=len(fence):
                        fence=None
                    continue
                if fence is not None:
                    continue
                # Exclude simple inline code and images; parse only explicit links.
                visible=re.sub(r'(\x60+).*?\1','',line)
                for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\((<[^>\n]+>|[^\s()\n]+)\)',visible):
                    token=match.group(1).strip('<>')
                    try:
                        url=urlsplit(token)
                    except ValueError:
                        continue
                    if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
                        continue
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(path),unquote(url.path)))
                    if target in paths:
                        references.append({'source':path,'target':target,'kind':'MARKDOWN_RELATIVE_LINK',
                                           'line':lineno,'token':token})
        else:
            unresolved.append({'source':path,'reason':'UNSUPPORTED_SOURCE_FORMAT'})
    return {'references':sorted(references,key=lambda r:(r['source'],r['line'],r['target'],r['kind'])),
            'unresolved':unresolved,'scope':'EXPLICIT_STATIC_REFERENCES_ONLY'}


# III. Native protected-constraint checks.
def _unit_job_failure(result, exceptions, expected_units):
    unit_jobs=result.get("UnitJobState")
    if not isinstance(unit_jobs,Mapping):
        return {
            "status":"OPEN",
            "blocker":"ARCHITECTURE_UNIT_JOB_STATE_MISSING",
            "result":result,
        }
    unit_job_evidence=result.get("UnitJobEvidence")
    if not unit_job_evidence:
        return {
            "status":"OPEN",
            "blocker":"ARCHITECTURE_UNIT_JOB_EVIDENCE_MISSING",
            "result":result,
        }
    try:
        reported_exceptions=_unit_ids(result.get("UnitJobExceptions",()))
    except ValueError:
        return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_EXCEPTIONS_INVALID","result":result}
    if reported_exceptions-exceptions:
        return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_EXCEPTIONS_UNAUTHORIZED:"+",".join(sorted(reported_exceptions-exceptions)),"result":result}
    if any(not isinstance(uid,str) or not uid.strip() for uid in unit_jobs):
        return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_IDS_INVALID","result":result}
    if expected_units is not None:
        observed=set(unit_jobs)
        if observed!=expected_units or len(observed)!=len(unit_jobs):
            return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_INVENTORY_MISMATCH","result":result,
                    "missing_units":tuple(sorted(expected_units-observed)),
                    "unexpected_units":tuple(sorted(observed-expected_units))}
    bad=[]
    for unit_id,raw_jobs in unit_jobs.items():
        uid=str(unit_id)
        if uid in exceptions:
            continue
        try:
            jobs=_normalized_jobs(raw_jobs)
        except ValueError:
            return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_IDENTITIES_INVALID:"+uid,"result":result}
        if len(jobs)>1:
            bad.append(uid+"="+"/".join(jobs))
    if bad:
        return {
            "status":"OPEN",
            "blocker":"ARCHITECTURE_UNIT_JOB_PURITY_VIOLATION:"+",".join(bad),
            "result":result,
        }
    return None


def _protected_constraint_failure(result, remaining):
    if remaining:
        state=result.get("ProtectedConstraintState")
        if not isinstance(state,Mapping):
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_PROTECTED_CONSTRAINT_STATE_MISSING",
                "result":result,
            }
        bad=[]
        for constraint_id in remaining:
            status=str(state.get(constraint_id,"MISSING")).upper()
            if status not in {"PRESERVED","PASS","VERIFIED"}:
                bad.append(f"{constraint_id}:{status}")
        if bad:
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_PROTECTED_CONSTRAINT_UNPRESERVED:"+",".join(bad),
                "result":result,
            }
    return None


# IV. Final architecture disposition.
def _architecture_status(result):
    boundary=result["OpenConflictBlocked"]
    if boundary:
        if isinstance(boundary,Mapping):
            labels={str(boundary.get(k,"")).upper() for k in ("status","state","disposition")}
            labels.update(str(k).upper() for k,v in boundary.items() if v and str(k).upper() in {"OPEN","BLOCKED","CONFLICT"})
        elif isinstance(boundary,(list,tuple,set,frozenset)):
            labels={str(x).upper() for x in boundary}
        else:
            labels={str(boundary).upper()}
        if "CONFLICT" in labels:
            status="CONFLICT"
        elif "BLOCKED" in labels:
            status="BLOCKED"
        else:
            status="OPEN"
    else:
        status="RELATIVE_CLOSE"

    return status

# V. Native architecture analysis orchestration.
def run_architecture_analysis(
    architecture:Any,
    contract:Any,
    *,
    analyze_architecture:Callable[[Any,Any],Mapping[str,Any]],
    protected_constraints:Iterable[str]=(),
)->dict[str,Any]:
    """Return the current AA_K(A) carrier while preserving OPEN/CONFLICT/BLOCKED."""
    if not callable(analyze_architecture):
        raise TypeError("ARCHITECTURE_ANALYZER_CALLABLE_REQUIRED")

    protected=tuple(dict.fromkeys(str(x) for x in protected_constraints if str(x)))
    # Freeze governing authority before invoking the external analyzer. The
    # optional contract fields are UnitJobExceptions and ExpectedUnitIds.
    exceptions=set()
    expected_units=None
    if UNIT_JOB_PURITY in protected and isinstance(contract,Mapping):
        try:
            exceptions=_unit_ids(contract.get("UnitJobExceptions",()))
            if "ExpectedUnitIds" in contract:
                expected_units=_unit_ids(contract["ExpectedUnitIds"])
        except ValueError:
            return {"status":"BLOCKED","blocker":"ARCHITECTURE_UNIT_JOB_CONTRACT_INVALID","result":None}

    raw=analyze_architecture(architecture,contract)
    if not isinstance(raw,Mapping):
        return {"status":"BLOCKED","blocker":"ARCHITECTURE_INVALID_RETURN","result":raw}

    result=dict(raw)
    missing=tuple(k for k in REQUIRED_OUTPUTS if k not in result)
    if missing:
        return {
            "status":"OPEN",
            "blocker":"ARCHITECTURE_OUTPUT_MISSING:"+",".join(missing),
            "result":result,
        }

    native_preserved=set()

    if UNIT_JOB_PURITY in protected:
        failure=_unit_job_failure(result,exceptions,expected_units)
        if failure is not None:
            return failure
        native_preserved.add(UNIT_JOB_PURITY)

    remaining=tuple(x for x in protected if x not in native_preserved)
    failure=_protected_constraint_failure(result,remaining)
    if failure is not None:
        return failure

    return {"status":_architecture_status(result),"result":result}
