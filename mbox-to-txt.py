import mailbox
import email
import sys
from email.header import decode_header

def convert_mbox_to_single_txt(mbox_path, output_path):
    """Convert MBOX to single text file"""
    mbox = mailbox.mbox(mbox_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, message in enumerate(mbox, 1):
            f.write(f"Email #{i}\n{'='*50}\n\n")
            
            for header in ['From', 'To', 'Subject', 'Date']:
                value = message.get(header, '')
                if value:
                    decoded_list = decode_header(value)
                    value = ''.join([str(t[0]) if isinstance(t[0], str) else t[0].decode(t[1] or 'utf-8') 
                                   for t in decoded_list])
                f.write(f"{header}: {value}\n")
            
            f.write("\n" + "-"*50 + "\n\n")
            
            if message.is_multipart():
                for part in message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
                        f.write(body + "\n")
            else:
                body = message.get_payload(decode=True).decode(message.get_content_charset() or 'utf-8', errors='replace')
                f.write(body + "\n")
            
            f.write("\n" + "="*50 + "\n\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input.mbox output.txt")
        sys.exit(1)
        
    mbox_path = sys.argv[1]
    output_path = sys.argv[2]
    convert_mbox_to_single_txt(mbox_path, output_path)
