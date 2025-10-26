/**
 * Campsite types available on Recreation.gov
 * These values come from the Recreation.gov API and must match exactly
 */
export const CAMPSITE_TYPES = [
  { value: '', label: 'Any Type (No Filter)' },
  { value: 'STANDARD NONELECTRIC', label: 'Standard Non-Electric' },
  { value: 'TENT ONLY NONELECTRIC', label: 'Tent Only Non-Electric' },
  { value: 'RV NONELECTRIC', label: 'RV Non-Electric' },
  { value: 'WALK TO', label: 'Walk-To Site' },
  { value: 'HIKE TO', label: 'Hike-In Site' },
  { value: 'GROUP TENT ONLY AREA NONELECTRIC', label: 'Group Tent Only Area Non-Electric' },
  { value: 'MANAGEMENT', label: 'Management Site' },
] as const;

/**
 * Get a human-readable label for a campsite type value
 */
export function getCampsiteTypeLabel(value: string): string {
  const type = CAMPSITE_TYPES.find(t => t.value === value);
  return type?.label || value;
}

