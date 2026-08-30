use tianheng::prelude::*;

pub fn representative_constitution() -> Constitution {
    Constitution::new("foundry-compatibility")
        .boundary(
            CrateBoundary::crate_("core")
                .deny_external_dependencies()
                .because("core declares no external dependencies"),
        )
        .boundary(
            ModuleBoundary::in_crate("app")
                .module("crate::domain")
                .must_not_import("crate::infra")
                .depth(ScanDepth::Subtree)
                .because("domain does not import infrastructure"),
        )
        .signature_boundary(
            SignatureBoundary::in_crate("app")
                .module("crate::api")
                .must_not_expose("crate::infra::DbPool")
                .because("the public API does not expose the database pool"),
        )
        .dyn_trait_boundary(
            DynTraitBoundary::in_crate("app")
                .module("crate::core")
                .must_not_expose_dyn()
                .because("the core public seam is statically dispatched"),
        )
        .trait_impl_boundary(
            TraitImplBoundary::in_crate("app")
                .trait_("crate::Command")
                .only_implemented_in("crate::commands")
                .because("command implementations live under commands"),
        )
        .visibility_boundary(
            VisibilityBoundary::in_crate("app")
                .module("crate::internal")
                .must_not_declare_pub()
                .because("internal remains crate-visible or narrower"),
        )
        .forbidden_marker_boundary(
            ForbiddenMarkerBoundary::in_crate("app")
                .module("crate::domain")
                .must_not_acquire("serde::Serialize")
                .because("domain types do not acquire wire markers"),
        )
        .unsafe_boundary(
            UnsafeBoundary::in_crate("app")
                .only_under(["crate::ffi"])
                .because("unsafe remains under the FFI subtree"),
        )
        .async_exposure_boundary(
            AsyncExposureBoundary::in_crate("app")
                .module("crate::core")
                .must_not_expose_async_fn()
                .including_submodules()
                .because("the core public surface remains synchronous"),
        )
        .runtime(
            RuntimeBoundary::at("adapter-seam")
                .only_origins(["app::adapters::blessed"])
                .because("only the blessed adapter crosses the seam"),
        )
        .sans_io_pure(
            SansIoPure::in_crate("app")
                .module("crate::kernel")
                .reading_clock_via("std::time", ["now"])
                .because("the kernel reads no ambient clock and exposes no async function"),
        )
}

// The 0.5.0 observation protocol, reached through the same public shell an adopter uses. Present
// because `shape-capability` now routes an adopter-owned house rule to it: a surface this
// repository sends someone to must be one the compatibility gate proves is there.

/// What each built-in dimension declares it does not observe.
///
/// `observation_bounds()` is not re-exported by the shell; the bounds are reachable anyway because
/// every dimension's observer delegates `Observer::bounds()` to it.
pub fn declared_observation_bounds() -> Vec<BoundDecl> {
    let constitution = representative_constitution();
    let mut bounds = StaticObserver::new(constitution.static_boundaries().clone()).bounds();
    bounds.extend(SemanticObserver::new(constitution.semantic_boundaries().clone()).bounds());
    bounds.extend(RuntimeObserver::new(constitution.runtime_boundaries().to_vec()).bounds());
    bounds
}

/// A house rule no dimension of 三儀 observes, owned by the adopter rather than upstream.
pub struct GovernedSubtreeObserver {
    subtrees: Vec<String>,
}

impl GovernedSubtreeObserver {
    pub fn reading<I: IntoIterator<Item = S>, S: Into<String>>(subtrees: I) -> Self {
        Self {
            subtrees: subtrees.into_iter().map(Into::into).collect(),
        }
    }
}

impl Observer for GovernedSubtreeObserver {
    fn observe(&self, manifest_path: &std::path::Path) -> Outcome {
        let Some(root) = manifest_path.parent() else {
            return Outcome::ConstitutionError("manifest has no parent directory".to_string());
        };
        let mut read = 0usize;
        for subtree in &self.subtrees {
            match std::fs::read_dir(root.join(subtree)) {
                Ok(entries) => read += entries.count(),
                Err(error) => {
                    return Outcome::ConstitutionError(format!(
                        "cannot read governed subtree '{subtree}': {error}"
                    ));
                }
            }
        }
        // `Subject::of` refuses to call a run clean when subtrees were declared and nothing was
        // read, so a failed look cannot be reported as a sound workspace.
        match Subject::of(self.subtrees.len(), read) {
            Some(subject) => Outcome::Clean(subject),
            None => Outcome::ConstitutionError(
                "subtrees were declared and no entry was read, so nothing was judged".to_string(),
            ),
        }
    }

    /// No default body exists for this: the protocol refuses a participant that will not state what
    /// it does not see.
    fn bounds(&self) -> Vec<BoundDecl> {
        vec![BoundDecl::pinned(
            BoundId::new("adopter/one-level-deep"),
            "an entry nested below the governed subtree",
            Extent::OutOfReach {
                because: "the walk reads one level deep, as this bound declares".into(),
            },
            "nested_entry_is_not_read",
        )]
    }
}

/// An adopter-owned observation composing into a run beside a built-in dimension.
pub fn composed_verdict(manifest_path: &std::path::Path) -> Outcome {
    Run::over(manifest_path)
        .observe(StaticObserver::new(
            representative_constitution().static_boundaries().clone(),
        ))
        .observe(GovernedSubtreeObserver::reading(["src"]))
        .verdict()
}
