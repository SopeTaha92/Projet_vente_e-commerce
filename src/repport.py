


import pandas as pd 
from loguru import logger
from typing import Dict


def repporting_excel(file : str, onglets : Dict[str , pd.DataFrame], min_orange, max_orange, green_value):
    """La fonction qui se charge de la génération des fichiers Excel"""
    with pd.ExcelWriter(file, engine='xlsxwriter') as writer:
        logger.info("Début de la génération du fichier Excel multi-onglets")
        workbook = writer.book
        base = {
            'align' : 'center',
            'valign' : 'center',
            'border' : 1
        }
        base_format = workbook.add_format(base)
        header_format = workbook.add_format(
            {
                **base,
                'bold' : True,
                'italic' : True,
                'bg_color' : "#5BDA42",
                'font_color' : 'white'
            }
        )
        money_format = workbook.add_format({**base, 'num_format' : '0.00" "€'})
        bonus_format = workbook.add_format({**base, 'num_format' : '0 %'})

        red_format = workbook.add_format({**base, 'bg_color' : '#FFC7CE'})
        orange_format = workbook.add_format({**base, 'bg_color' : '#FFEB9C'})
        green_format = workbook.add_format({**base, 'bg_color' : '#13FF3A'})

        for name, data in onglets.items():
            data.to_excel(writer, sheet_name=name, index=False)
            logger.info(f"Début de la génération du feuille {name}")
            worksheet = writer.sheets[name]
            for column_numb, value in enumerate(data.columns):
                worksheet.write(0, column_numb, value, header_format)
            logger.info(f"Application du formatage de l'entete sur la feuille {name}")
            worksheet.freeze_panes(1, 0)
            logger.info(f"Fixation de l'entete sur la feuille {name}")
            worksheet.autofilter(0, 0, len(data), len(data.columns) - 1)
            logger.info(f"Application de l'auto_filter sur la feuille {name}")
            column_money = ['unit_price', 'total_price', 'Montant_remise', 'Ca_Net']
            for i, column in enumerate(data.columns):
                column_letter = data[column].astype(str).str.len().max()
                column_letter = max(column_letter, len(column)) + 3
                if column == 'discount':
                    worksheet.set_column(i, i, column_letter, bonus_format)
                elif column in column_money:
                    worksheet.set_column(i, i, column_letter, money_format)
                else:
                    worksheet.set_column(i, i, column_letter, base_format)


                if 'Montant_remise' in data.columns:
                        profit_column = data.columns.get_loc('Montant_remise')
                        worksheet.conditional_format(1, profit_column, len(data), profit_column, {
                            'type' : 'cell',
                            'criteria' : '<=',
                            'value' : 0,
                            'format' : red_format
                        })

                        worksheet.conditional_format(1, profit_column, len(data), profit_column, {
                            'type' : 'cell',
                            'criteria' : 'between',
                            'minimum' : min_orange, 
                            'maximum' : max_orange,
                            'format' : orange_format
                        })

                        worksheet.conditional_format(1, profit_column, len(data), profit_column, {
                            'type' : 'cell',
                            'criteria' : '>',
                            'value' : green_value,#100000,
                            'format' : green_format
                        })
            if name == 'Données Par Catégories':

                logger.info(f"Début de la création du graphique pour la feuille {name}")
                chart_col = workbook.add_chart({'type' : 'column'})
                chart_line = workbook.add_chart({'type' : 'line'})
                category_column = data.columns.get_loc('category')
                Ca_Net_column = data.columns.get_loc('Ca_Net')
                quantity_column = data.columns.get_loc('quantity')
        
                chart_col.add_series(
                    {
                        'name' : 'Ca_Net',
                        'categories' : [name, 1, category_column, len(data), category_column],
                        'values' : [name, 1, Ca_Net_column, len(data), Ca_Net_column]
                    }
                )

                chart_line.add_series(
                    {
                        'name' : 'quantity',
                        'categories' : [name, 1, category_column, len(data), category_column],
                        'values' : [name, 1, quantity_column, len(data), quantity_column],
                        'y2_axis' : True
                    }
                )
                chart_col.combine(chart_line)
                chart_col.set_title({'name' : 'Répartition Ca_Net / quantité'})
                worksheet.insert_chart(1, data.shape[1] + 1, chart_col)
                logger.info(f"Graphique crée avec succée pour la feuille {name}")


            if name == 'Données Par Status':
                logger.info(f"Début de la création du graphique pour la feuille {name}")
                chart_col = workbook.add_chart({'type' : 'column'})
                chart_line = workbook.add_chart({'type' : 'line'})
                status_column = data.columns.get_loc('status')
                Ca_Net_column = data.columns.get_loc('Ca_Net')
                Montant_remise_column = data.columns.get_loc('Montant_remise')
                quantity_column = data.columns.get_loc('quantity')

                chart_col.add_series(
                    {
                        'name' : 'Ca_Net',
                        'categories' : [name, 1, status_column, len(data), status_column],
                        'values' : [name, 1, Ca_Net_column, len(data), Ca_Net_column]
                    }
                )

                chart_col.add_series(
                    {
                        'name' : 'Montant_remise',
                        'categories' : [name, 1, status_column, len(data), status_column],
                        'values' : [name, 1, Montant_remise_column, len(data), Montant_remise_column]
                    }
                )
        
                chart_line.add_series(
                    {
                        'name' : 'quantity',
                        'categories' : [name, 1, status_column, len(data), status_column],
                        'values' : [name, 1, quantity_column, len(data), quantity_column],
                        'y2_axis' : True
                    }
                )

                chart_col.combine(chart_line)
                worksheet.insert_chart(1, data.shape[1] + 1, chart_col)
                logger.info(f"Graphique crée avec succée pour la feuille {name}")


            if name == 'Données Par City':
                logger.info(f"Début de la création du graphique pour la feuille {name}")
                chart_pie = workbook.add_chart({'type' : 'pie'})
                shipping_city_column = data.columns.get_loc('shipping_city')
                Ca_Net_column = data.columns.get_loc('Ca_Net')

                chart_pie.add_series(
                    {
                        'name' : 'shipping_city',
                        'categories' : [name, 1, shipping_city_column, len(data), shipping_city_column],
                        'values' : [name, 1, Ca_Net_column, len(data), Ca_Net_column],
                        'data_labels' : {'percentage' : True,'category' : True,'position' : 'outside_end'}
                    }                
                )
                chart_pie.set_legend({'position' : 'none'})
                chart_pie.set_title({'name' : 'Répartition du Ca_Net par Région'})
                worksheet.insert_chart(1, data.shape[1] + 1, chart_pie)
                logger.info(f"Graphique crée avec succée pour la feuille {name}")

        logger.success(f"Feuille Excel de Repporting {name} crée avec succée")

    logger.success(f"Fichier Excel de Repporting {file.name} a étais crée avec succée")





    print(f"Fichier {file.name} crée avec succée")



