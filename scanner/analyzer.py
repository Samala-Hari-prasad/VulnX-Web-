def analyze_response(response, payload, vuln_type):
    if not response:
        return False
        
    text = response.text.lower()
    
    if vuln_type == 'SQLi':
        sql_errors = [
            "sql syntax",
            "mysql_fetch_array",
            "ora-01756",
            "postgresql query failed",
            "unclosed quotation mark after the character string"
        ]
        for error in sql_errors:
            if error in text:
                return True
                
    elif vuln_type == 'XSS':
        if payload.lower() in text:
            return True
            
    return False
