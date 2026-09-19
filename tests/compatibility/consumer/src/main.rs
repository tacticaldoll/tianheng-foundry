//! The adopter-facing runner shape: one declared Constitution handed to `tianheng::run`.
//!
//! Foundry's skills instruct an agent to drive this surface — `list --format json` for the
//! declared law, `check --format json` for the reaction, and the exit classes both are read
//! by — so the compatibility gate exercises it rather than only compiling the vocabulary the
//! Constitution is built from.
//!
//! `FOUNDRY_FIXTURE_CONSTITUTION` selects which declaration to run, because `run` consumes the
//! whole argument list and a mode argument would collide with the invocation shapes under test.

use std::process::ExitCode;

use tianheng_foundry_compatibility as fixture;

fn main() -> ExitCode {
    let constitution = match std::env::var("FOUNDRY_FIXTURE_CONSTITUTION").as_deref() {
        Ok("clean") => fixture::clean_constitution(),
        Ok("violating") => fixture::violating_constitution(),
        _ => fixture::representative_constitution(),
    };
    tianheng::run(&constitution, std::env::args())
}
