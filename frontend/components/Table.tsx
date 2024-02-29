import { Column } from "@/index";

interface TableProps {
  columns: Column[];
  rows: any[];
  handleDelete: (id: number) => void;
}

export default function Table({ columns, rows, handleDelete }: TableProps) {
  return (
    <>
      <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5">
        <div className="relative w-full overflow-auto">
          <table className="w-full caption-bottom text-sm">
            <thead className="[&amp;_tr]:border-b">
              <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                {columns.map((c) => (
                  <th
                    key={c.label}
                    className="h-12 px-4 text-left align-middle font-medium text-muted-foreground [&amp;:has([role=checkbox])]:pr-0"
                  >
                    {c.label}
                  </th>
                ))}
                <th className="h-12 px-4 text-right align-middle font-medium text-muted-foreground [&amp;:has([role=checkbox])]:pr-0"></th>
              </tr>
            </thead>
            <tbody className="[&amp;_tr:last-child]:border-0">
              {rows.length > 0 ? (
                rows.map((row, i) => (
                  <tr
                    key={i}
                    className="border-b transition-colors hover:bg-grey-50 data-[state=selected]:bg-muted"
                  >
                    {columns.map((column) => (
                      <td
                        className="p-4 align-middle [&amp;:has([role=checkbox])]:pr-0 font-medium"
                        key={column.id}
                      >
                        {row[column.id]}
                      </td>
                    ))}
                    <td className="p-4 text-right align-middle [&amp;:has([role=checkbox])]:pr-0">
                      <button
                        className="inline-flex border-red-100 items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-10 px-2 py-2"
                        onClick={() => handleDelete(row.id)}
                      >
                        Usuń
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                  <td className="p-4 align-middle [&amp;:has([role=checkbox])]:pr-0 font-medium">
                    Brak elementów do wyświetlenia.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
