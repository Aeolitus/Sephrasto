#!/usr/bin/env python3
"""
Script to add UUIDs to all database elements in the XML file.
This directly modifies the XML file to add id attributes to all elements.
"""

import xml.etree.ElementTree as ET
import uuid
import os

def add_ids_to_xml():
    """Add UUIDs to all database elements in the XML file."""
    xml_file = os.path.join('src', 'Sephrasto', 'Data', 'datenbank.xml')
    
    if not os.path.exists(xml_file):
        print(f"Error: Database file not found: {xml_file}")
        return False
    
    print(f"Loading XML file: {xml_file}")
    
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Elements that should get IDs
    element_types = [
        'Attribut', 'AbgeleiteterWert', 'Energie', 'Vorteil', 'Talent', 
        'Fertigkeit', 'UeberFertigkeit', 'Waffe', 'Ruestung', 'Regel', 
        'Waffeneigenschaft', 'FreieFertigkeit'
    ]
    
    total_updated = 0
    
    for element_type in element_types:
        elements = root.findall(element_type)
        updated_count = 0
        
        for element in elements:
            # Check if element already has an id
            if 'id' not in element.attrib:
                # Generate a new UUID
                new_id = str(uuid.uuid4())
                element.set('id', new_id)
                updated_count += 1
        
        if updated_count > 0:
            print(f"Added IDs to {updated_count} {element_type} elements")
        total_updated += updated_count
    
    if total_updated > 0:
        # Create backup
        backup_file = xml_file + '.backup'
        print(f"Creating backup: {backup_file}")
        import shutil
        shutil.copy2(xml_file, backup_file)
        
        # Save the modified XML
        print(f"Saving updated XML file...")
        tree.write(xml_file, encoding='UTF-8', xml_declaration=True)
        
        print(f"Successfully added IDs to {total_updated} elements!")
        print(f"Backup created at: {backup_file}")
    else:
        print("All elements already have IDs - no changes needed.")
    
    return True

if __name__ == "__main__":
    try:
        add_ids_to_xml()
    except Exception as e:
        print(f"Error updating XML: {e}")
        import traceback
        traceback.print_exc() 