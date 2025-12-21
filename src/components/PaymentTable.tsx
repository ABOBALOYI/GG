interface PaymentDate {
  method: 'cash' | 'bank' | 'post_office';
  startDate: string;
  endDate: string;
}

interface PaymentTableProps {
  grantName: string;
  paymentDates: PaymentDate[];
  notes?: string;
}

const methodLabels: Record<string, string> = {
  cash: 'Cash (Pay Point)',
  bank: 'Bank Account',
  post_office: 'Post Office',
};

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-ZA', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  });
}

export default function PaymentTable({ grantName, paymentDates, notes }: PaymentTableProps) {
  return (
    <div className="my-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">{grantName}</h3>
      <div className="overflow-x-auto">
        <table className="min-w-full border border-gray-200 rounded-lg overflow-hidden">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-4 py-3 text-left text-sm font-semibold text-gray-900">
                Collection Method
              </th>
              <th scope="col" className="px-4 py-3 text-left text-sm font-semibold text-gray-900">
                Start Date
              </th>
              <th scope="col" className="px-4 py-3 text-left text-sm font-semibold text-gray-900">
                End Date
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 bg-white">
            {paymentDates.map((payment, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm text-gray-900">
                  {methodLabels[payment.method] || payment.method}
                </td>
                <td className="px-4 py-3 text-sm text-gray-700">
                  {formatDate(payment.startDate)}
                </td>
                <td className="px-4 py-3 text-sm text-gray-700">
                  {formatDate(payment.endDate)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {notes && (
        <p className="mt-2 text-sm text-gray-600 italic">{notes}</p>
      )}
    </div>
  );
}
