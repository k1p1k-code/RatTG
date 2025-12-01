use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Deserialize)]
pub struct JSONResponsePolling {
    pub tasks: Vec<HashMap<String, Option<String>>>,
}
