def build_filtered_csv_export(df, start_idx, end_idx, rsi_min, rsi_max, macd_min, macd_max, macd_sig_min, macd_sig_max, volumen_slider_min=None, volumen_slider_max=None):
    if 'Volume' in df.columns or 'volume' in df.columns:
        vol_col = 'Volume' if 'Volume' in df.columns else 'volume'
        volume_min = float(df[vol_col].min())
        volume_max = float(df[vol_col].max())
    else:
        volume_min = volumen_slider_min or ""
        volume_max = volumen_slider_max or ""

    filter_metadata = [
        "\n# Filtros aplicados",
        "Indicador,Mínimo,Máximo",
        f"RSI,{rsi_min},{rsi_max}",
        f"MACD,{macd_min},{macd_max}",
        f"MACD Signal,{macd_sig_min},{macd_sig_max}",
        f"Volumen,{volume_min},{volume_max}"
    ]
    filter_metadata_str = "\n".join(filter_metadata)
    csv_data = df.iloc[start_idx:end_idx].to_csv(index=False)
    full_csv = f"{csv_data}\n{filter_metadata_str}"
    return full_csv.encode("utf-8")