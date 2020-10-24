function relatorio(){
    const doc = new jsPDF({orientation: 'landscape'});

    const texto = document.getElementById('dados').innerText;
    const arrLinhas = texto.split('#');
    let conteudo = 'RELATÓRIO DE FRIOS\n\n';
    for(let linha = 0; linha < arrLinhas.length; linha++){
        let arrColunas = arrLinhas[linha].split('|');
        arrColunas[0] = arrColunas[0].trim().padEnd(35, '*');
        if(arrColunas[0].indexOf('*') > 0){
            conteudo += `ID: ${arrColunas[0]} - ` + 
                        `NOME: ${arrColunas[1]} - ` + 
                        `QUANTIDADE: ${arrColunas[2]} - ` + 
                        `PREÇO: R$ ${arrColunas[3]}\n\n`;
        }
    }
    doc.setFontSize(12);
    doc.setFont('Courier');
    doc.text(conteudo, 30, 30);
    doc.save('relatório.pdf');
}