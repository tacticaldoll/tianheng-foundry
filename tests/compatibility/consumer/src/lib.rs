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
            SemanticBoundary::in_crate("app")
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
