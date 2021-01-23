import { format } from 'date-fns'
import { enGB } from 'date-fns/locale'

export function formatDate(value) {
  return format(new Date(value), 'Pp', { locale: enGB })
}